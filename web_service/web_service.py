from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# API URL'sini daha temiz tanımlayalım
API_URL = "https://hello-cloud4.onrender.com/ziyaretciler"

HTML = """
<!doctype html>
<html>
<head>
 <title>Mikro Hizmetli Selam!</title>
 <style>
 body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
 h1 { color: #333; }
 input { padding: 10px; font-size: 16px; }
 button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
 li { background: white; list-style: none; margin: 5px auto; width: 250px; padding: 8px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
 ul { padding: 0; }
 </style>
</head>
<body>
 <h1>Mikro Hizmetli Selam!</h1>
 <form method="POST">
 <input type="text" name="isim" placeholder="Adınızı yaz" required>
 <button type="submit">Gönder</button>
 </form>
 <h3>Son Ziyaretçiler:</h3>
 <ul>
 {% for ad in isimler %}
 <li>{{ ad }}</li>
 {% else %}
 <li>Henüz kimse gelmedi.</li>
 {% endfor %}
 </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        try:
            # API'ye veriyi gönder
            requests.post(API_URL, json={"isim": isim}, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"API Hatası (POST): {e}")
        
        # İşlem bittikten sonra sayfayı yenilemek için yönlendir
        return redirect("/")

    # GET İsteği: API'den listeyi çek
    isimler = []
    try:
        resp = requests.get(API_URL, timeout=5)
        if resp.status_code == 200:
            isimler = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API Hatası (GET): {e}")

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    # Render gibi platformlar portu dışarıdan verir
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
