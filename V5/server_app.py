from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "senzor_podaci.db"


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/data")
def get_data():
  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    cursor.execute("""
            SELECT timestamp, value 
            FROM merenja 
            ORDER BY id DESC 
            LIMIT 20
        """)
    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    timestamps = [row[0] for row in rows]
    values = [row[1] for row in rows]

    return jsonify({"timestamps": timestamps, "values": values})

  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5001)