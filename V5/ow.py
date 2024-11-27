import sys
import requests
from time import sleep

baseURL = 'https://api.openweathermap.org/data/2.5/weather?lat=45.267136&lon=19.833549&appid=7c51a71a9d058401ec4990f513bfd83f&units=metric'

conn = requests.get(baseURL)

data = conn.json()

print(data)

temp = data["main"]["temp"]
temp_min = data["main"]["temp_min"]
temp_max = data["main"]["temp_max"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]

print("trenutna: %s, min: %s, max: %s, vlaznost: %s, brzina vetra: %s" %(temp, temp_min, temp_max, humidity, wind_speed))