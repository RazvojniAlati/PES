import datetime
import sqlite3
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "uredjaj/senzor/temperatura"
DB_NAME = "senzor_podaci.db"


def init_db():
 
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS merenja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            topic TEXT NOT NULL,
            value REAL NOT NULL
        )
    """)
  conn.commit()
  conn.close()


def save_to_db(topic, value):
  
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO merenja (timestamp, topic, value) VALUES (?, ?, ?)",
        (timestamp, topic, float(value)),
    )
    conn.commit()
    conn.close()
    print("[BAZA] Podatak uspešno sačuvan u bazu.")
  except ValueError:
    print(
        "[BAZA] Greška: Primljeni podatak nije broj, nije sačuvan u bazu."
    )
  except Exception as e:
    print(f"[BAZA] Greška prilikom upisa: {e}")


def on_message(client, userdata, msg):
  payload = msg.payload.decode("utf-8")
  print(f"[PRIMLJENO] Tema: {msg.topic} ---> Vrednost: {payload}")


  save_to_db(msg.topic, payload)


def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Uspešno povezan sa brokerom!")
    client.subscribe(TOPIC)
    print(f"Pretplaćen na temu: '{TOPIC}'. Čekanje dolaznih poruka...\n")
  else:
    print(f"Konekcija nije uspela, kod greške: {rc}")


if __name__ == "__main__":
  init_db()

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