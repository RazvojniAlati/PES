import sys
import urllib.request as urllib2
from time import sleep
import math

myAPI = 'R9AUPF28BC18KLUL'

baseURL = 'httpS://api.thingspeak.com/update?api_key=%s' % myAPI

br = 0;
temp = [1, 4, 7, 5, 3, 2, 6, 3, 1, 8, 3, 5]
humi = [1, 12, 7, 2, 3, -4, 6, 3, 10, 8, 6, 5]

while True:
    
    conn = urllib2.urlopen(baseURL + '&field1=%s&filed2=%s' % (temp[br], humi[br]))
    print(conn.read())
    conn.close()
    
    br = br+1
    
    if(br == 12):
        br = 0
    
    sleep(1)
