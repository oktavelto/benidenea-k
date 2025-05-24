from flask import Flask, render_template, request, session
from fal_integration import run_fal

app = Flask(__name__)
app.secret_key = "gizli_key"

@app.route("/")
def index():
    session["deneme_sayisi"] = 0
    return render_template("index.html")

@app.route("/dene", methods=["POST"])
def dene():
    if session.get("deneme_sayisi", 0) >= 2:
        return render_template("limit.html")

    secim = request.form["model_secimi"]
    garment_url = request.form["garment_image_url"]

    if secim == "ozel":
        human_url = request.form["ozel_model_url"]
    else:
        human_url = f"/static/models/{secim}"

    output = run_fal(human_url, garment_url)
    session["deneme_sayisi"] += 1
    return render_template("result.html", result=output)

if __name__ == "__main__":
    app.run(debug=True)
