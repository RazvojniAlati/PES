import sys
import requests
from time import sleep

baseURL = 'https://api.openweathermap.org/data/2.5/onecall?lat=45.267136&lon=19.833549&exclude=minutely,hourly&appid=0c405018ba2dd0fa820d2348df2b542e&units=metric'

conn = requests.get(baseURL)

data = conn.json()

print(data)

temp = data["current"]["temp"]
temp_min = data["daily"][0]["temp"]["min"]
temp_max = data["daily"][0]["temp"]["max"]
humidity = data["current"]["humidity"]
wind_speed = data["current"]["wind_speed"]

print("trenutna: %s, min: %s, max: %s, vlaznost: %s, bryina vetra: %s" %(temp, temp_min, temp_max, humidity, wind_speed))

