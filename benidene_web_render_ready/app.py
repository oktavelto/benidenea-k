
from flask import Flask, render_template, request
import asyncio
import fal_client

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/dene", methods=["POST"])
def dene():
    model_secimi = request.form.get("model_secimi")
    if model_secimi == "ozel":
        human_image_url = request.form.get("ozel_model_url")
    else:
        human_image_url = f"/static/models/{model_secimi}"

    garment_image_url = request.form.get("garment_image_url")

    if not human_image_url or not garment_image_url:
        return "Görseller eksik.", 400

    async def process():
        stream = fal_client.stream_async(
            "workflows/oktavelto/fasn",
            arguments={
                "human_image_url": human_image_url,
                "garment_image_url": garment_image_url
            },
        )
        async for event in stream:
            print(event)
        result = await stream.done()
        return result["image"]["url"]

    try:
        output_url = asyncio.run(process())
    except Exception as e:
        return f"Hata oluştu: {e}"

    return f"<h2>Sonuç Görseli:</h2><img src='{output_url}' style='max-width:100%;'>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
