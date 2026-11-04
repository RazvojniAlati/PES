import random
import time
import paho.mqtt.client as mqtt


BROKER = "localhost"  
PORT = 1883
TOPIC = "uredjaj/senzor/temperatura"


client = mqtt.Client()

try:
    print(f"Povezivanje sa MQTT brokerom na {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
    client.loop_start() 

    print(f"Započeto slanje podataka na temu: '{TOPIC}'. Pritisni Ctrl+C za izlaz.\n")

    while True:
        
        temperatura = round(random.uniform(20.0, 30.0), 2)
        
        
        info = client.publish(TOPIC, str(temperatura))
        info.wait_for_publish()  
        
        print(f"Poslato -> Tema: {TOPIC} | Vrednost: {temperatura}")
        
        time.sleep(2)  

except KeyboardInterrupt:
    print("\nPrekid od strane korisnika. Zatvaranje konekcije...")
    client.loop_stop()
    client.disconnect()
    print("Klijent za slanje je ugašen.")