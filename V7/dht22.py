import datetime
import json
import time
import adafruit_dht
import board
import paho.mqtt.client as mqtt


BROKER = "localhost"  
PORT = 1883
TOPIC = "uredjaj/senzor/podaci"
PUBLISH_INTERVAL = 2.0  


dht_device = adafruit_dht.DHT22(board.D4)


def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print(f"[MQTT] Povezan na broker {BROKER}:{PORT}")
  else:
    print(f"[MQTT] Greška pri povezivanju, kod: {rc}")


def main():
  client = mqtt.Client()
  client.on_connect = on_connect

  client.connect(BROKER, PORT, 60)
  client.loop_start()

  print(f"[DHT22] Pokrenuto objavljivanje na temu '{TOPIC}' (Ctrl+C za prekid)\n")

  try:
    while True:
      try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        if temperature_c is not None and humidity is not None:
          payload_dict = {
              "timestamp": datetime.datetime.now().strftime(
                  "%Y-%m-%d %H:%M:%S"
              ),
              "temperatura": round(float(temperature_c), 1),
              "vlaznost": round(float(humidity), 1),
          }
          payload_json = json.dumps(payload_dict)

          result = client.publish(TOPIC, payload_json)
          if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[POSLATO] {payload_json}")
          else:
            print(f"[MQTT] Neuspešno slanje, kod: {result.rc}")

      except RuntimeError as err:
        print(f"[DHT22] Privremena greška pri očitavanju: {err.args[0]}")

      time.sleep(PUBLISH_INTERVAL)

  except KeyboardInterrupt:
    print("\n[INFO] Zaustavljam publisher...")
  finally:
    client.loop_stop()
    client.disconnect()
    dht_device.exit()
    print("[INFO] Resursi oslobođeni.")


if __name__ == "__main__":
  main()