from machine import I2C, Pin, PWM
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import uasyncio as asyncio
from config import RotatorConfig as CFG

azimuth = -1
target = -1

correction = CFG.AZ_CORRECTION
pwmPin = Pin(CFG.PWM_PIN)
dirPin = Pin(CFG.DIR_PIN, Pin.OUT)
enPin = Pin(CFG.EN_PIN, Pin.OUT)
DIRCW = CFG.DIRCW
DIRCCW = CFG.DIRCCW
ROTENABLE = CFG.ROTENABLE
ROTDISABLE = CFG.ROTDISABLE
FREQ_LO  = CFG.FREQ_LO
FREQ_MID = CFG.FREQ_MID
FREQ_HI = CFG.FREQ_HI
ROT_THRESHOLD_HI = CFG.ROT_THRESHOLD_HI
ROT_THRESHOLD_LO = CFG.ROT_THRESHOLD_LO

enPin.value(ROTDISABLE)

# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'
i2c = I2C(0, scl=Pin(CFG.I2C_SCL_PIN), sda=Pin(CFG.I2C_SDA_PIN), freq=400000)


# root route
@app.route('/')
async def index(request):
    return render_template('index.html')


@app.route('/ws')
@with_websocket
async def read_sensor(request, ws):
    #print("read /ws")
    global azimuth
    global target
    while True:
        data = await ws.receive()
        try:
            tmp = int(data)
            if tmp >= -1 and tmp < 360:
                target = tmp
        except:
            pass
        await ws.send(str(azimuth))


# Static CSS/JS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


async def update_az():
    global azimuth
    #Read raw angle
    while True:
        try:
            bytes = i2c.readfrom_mem(0x36, 0xC, 2)
        except:
            azimuth = -1
            #print("read error")
        else:
            rawangle = int.from_bytes(bytes, 'big') & 0xFFF
            tazimuth = round(rawangle * 360 / 4096)
            if CFG.AS_DIR_INVERT:
                tazimuth = 360 - tazimuth
            tazimuth += correction
            if tazimuth >= 360: tazimuth -= 360
            elif tazimuth < 0: tazimuth += 360
            azimuth = tazimuth
            #print(f"{azimuth=}")
        await asyncio.sleep(0.1)


async def pwm_proc():
    global target
    global azimuth
    outpwm = None
    while True:
        if target != -1:
            if azimuth == -1 or target == azimuth:
                target = -1
            else:
                #print(f"{azimuth=}, setting up for {target=}")
                target_s = target
                if target_s < azimuth:
                    dirPin.value(DIRCCW)
                    dir = DIRCCW
                    #print("Dir=CCW")
                else:
                    dirPin.value(DIRCW)
                    dir = DIRCW
                    #print("Dir=CW")
                frequency = FREQ_LO
                outpwm = PWM(pwmPin, freq=frequency, duty=512)
                #print(f"{frequency=}")
                enPin.value(ROTENABLE)
                #print("En=On")
                rot_diff = max(target_s, azimuth) - min(target_s, azimuth)
                if rot_diff >= ROT_THRESHOLD_HI: #Start at slow speed
                    await asyncio.sleep(1)
                while True:
                    await asyncio.sleep(0.02)
                    if target_s != target:
                        #print("Target has changed")
                        break
                    if ( target_s == azimuth or
                         (dir == DIRCW and target_s < azimuth) or
                         (dir == DIRCCW and target_s > azimuth) ):
                        #print("Azimuth reached the target")
                        target = -1
                        break
                    rot_diff = max(target_s, azimuth) - min(target_s, azimuth)
                    if rot_diff < ROT_THRESHOLD_LO:
                        if frequency != FREQ_LO:
                            frequency = FREQ_LO
                            outpwm.freq(frequency)
                            #print(f"upd {frequency=}")
                    elif rot_diff < ROT_THRESHOLD_HI:
                        if frequency != FREQ_MID:
                            frequency = FREQ_MID
                            outpwm.freq(frequency)
                            #print(f"upd {frequency=}")
                    else:
                        if frequency != FREQ_HI:
                            frequency = FREQ_HI
                            outpwm.freq(frequency)
                            #print(f"upd {frequency=}")
        if outpwm:
            enPin.value(ROTDISABLE)
            #print("En=Off")
            outpwm.deinit()
            outpwm = None
        await asyncio.sleep(0.1)


async def server_main():
    await app.start_server(port=80, debug=False)


async def __main():
    tasks = [server_main(), update_az(), pwm_proc()]
    ret = await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(__main())
    except KeyboardInterrupt:
        pass
    gc.collect()
    print("Exit main.py")
