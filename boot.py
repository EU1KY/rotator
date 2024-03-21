from machine import reset
import sys
sys.path.reverse()
import esp
esp.osdebug(None)
import network
import gc
from config import RotatorConfig as CFG
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(CFG.WIFI_SSID, CFG.WIFI_PASSWD)
while station.isconnected() == False:
    pass
#print('WiFi connection successful')
print(station.ifconfig())
gc.enable()
import uftpd
