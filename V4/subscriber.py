import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TOPIC = "uredjaj/senzor/temperatura"


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[PRIMLJENO] Tema: {msg.topic} ---> Vrednost: {payload}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Uspešno povezan sa brokerom!")
        client.subscribe(TOPIC)
        print(f"Pretplaćen na temu: '{TOPIC}'. Čekanje dolaznih poruka...\n")
    else:
        print(f"Konekcija nije uspela, kod greške: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Povezivanje sa MQTT brokerom na {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
    
    client.loop_forever()

except KeyboardInterrupt:
    print("\nPrekid od strane korisnika. Gasim subscriber...")
    client.disconnect()
    print("Subscriber je ugašen.")