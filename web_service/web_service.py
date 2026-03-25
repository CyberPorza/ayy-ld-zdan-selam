from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

API_URL = "https://ayy-ld-zdan-selam-2.onrender.com"

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
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
        .hata { color: red; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adını yaz</p>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <button type="submit">Gönder</button>
    </form>
    {% if hata %}
        <p class="hata">{{ hata }}</p>
    {% endif %}
    <h3>Ziyaretciler:</h3>
    <ul>
        {% for ad in isimler %}
            <li>{{ ad }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    hata = None

    if request.method == "POST":
        isim = request.form.get("isim", "").strip()
        if isim:
            try:
                requests.post(
                    API_URL + "/ziyaretciler",
                    json={"isim": isim},
                    timeout=5
                )
            except requests.exceptions.RequestException:
                hata = "API'ye bağlanılamadı, lütfen tekrar deneyin."
        return redirect("/")

    isimler = []
    try:
        resp = requests.get(API_URL + "/ziyaretciler", timeout=5)
        if resp.status_code == 200:
            isimler = resp.json()
        else:
            hata = "Ziyaretçi listesi alınamadı."
    except requests.exceptions.RequestException:
        hata = "API'ye bağlanılamadı."

    return render_template_string(HTML, isimler=isimler, hata=hata)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
