from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://porza:C8gpGxYMVrbkPtvAY0aA3V1MQwTu68ck@dpg-d6t8qqdm5p6s73b7u9dg-a.oregon-postgres.render.com/hello_cloud_2_4p3d"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretçiler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    
    # SERIAŞ yerine SERIAL düzeltildi
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            # Büyük S küçük s yapıldı ve (isim,) şeklinde tuple'a çevrildi
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            # commmit()
