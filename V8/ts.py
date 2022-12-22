import urequests
import network, time

ssid = 'Redmi Note 10 Pro'
password = '06eaa600497e'

myAPI = 'D3GA4YLJLUCYLGIS'

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

# Configure ESP32 as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
     pass
print('network config:', sta_if.ifconfig())

br = 0;
temp = [1, 4, 7, 5, 3, 2, 6, 3, 1, 8, 3, 5]
humi = [1, 12, 7, 2, 3, -4, 6, 3, 10, 8, 6, 5]

while True:
    
    conn = urequests.post(baseURL + '&field1=%s&filed2=%s' % (temp[br], humi[br]))
    #print(conn.read())
    conn.close()
    
    br = br+1
    
    if(br == 12):
        br = 0
    
    time.sleep(1)


