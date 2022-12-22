# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import time
from mqttsimple import MQTTClient
import ubinascii
import micropython
import netAwork
import esp
esp.osdebug(None)
gc.collect()
#import webrepl
#webrepl.start()
ssid = 'Redmi Note 10 Pro'
password = '06eaa600497e'
mqtt_server = '192.168.128.83'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())



