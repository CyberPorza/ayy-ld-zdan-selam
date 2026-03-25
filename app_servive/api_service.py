from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
import os

app = Flask(__name__)
CORS(app)

# DATABASE_URL'i mutlaka ortam değişkeninden al, default değer bırakma!
DATABASE_URL = os.getenv("postgresql://porza:C8gpGxYMVrbkPtvAY0aA3V1MQwTu68ck@dpg-d6t8qqdm5p6s73b7u9dg-a.oregon-postgres.render.com/hello_cloud_2_4p3d")

# Bağlantı havuzu oluşturma (Min 1, Max 10 bağlantı)
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
except Exception as e:
    print(f"Veritabanı havuzu oluşturulamadı: {e}")

def init_db():
    """Tabloyu uygulama başlarken bir kez oluşturur."""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")
            conn.commit()
    finally:
        db_pool.putconn(conn)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            if request.method == "POST":
                data = request.get_json()
                isim = data.get("isim")
                if isim and len(isim.strip()) > 0:
                    cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim.strip(),))
                    conn.commit()
                else:
                    return jsonify({"error": "İsim alanı boş olamaz"}), 400

            cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
            isimler = [row[0] for row in cur.fetchall()]
            return jsonify(isimler)
            
    except Exception as e:
        return jsonify({"error": "Sunucu hatası oluştu", "details": str(e)}), 500
    finally:
        if conn:
            db_pool.putconn(conn)

if __name__ == "__main__":
    init_db() # Tabloyu kontrol et
    app.run(host="0.0.0.0", port=5001, debug=False) # Production'da debug=False olmalı
