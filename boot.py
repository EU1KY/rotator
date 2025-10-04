from machine import reset, Pin
import sys
sys.path.reverse()
import esp
esp.osdebug(None)
import network
import gc
from config import RotatorConfig as CFG

# 1st thing to do: remove Enable signal from the stepper motor controler.
enPin = Pin(CFG.EN_PIN, Pin.OUT)
enPin.value(CFG.ROTDISABLE)

station = network.WLAN(network.STA_IF)
station.active(True)
station.config(dhcp_hostname = CFG.HOSTNAME)
station.connect(CFG.WIFI_SSID, CFG.WIFI_PASSWD)
while station.isconnected() == False:
    pass
#print('WiFi connection successful')
print(station.ifconfig())
gc.enable()
import uftpd
