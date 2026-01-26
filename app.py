from flask import Flask, render_template, request
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

app = Flask(__name__)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def style_caption(caption, style):
    if style == "funny":
        return f"😂 {caption} — looks like it’s having a great day!"
    elif style == "dramatic":
        return f"🎭 In a world of silence… {caption}."
    else:  # professional
        return caption

@app.route("/", methods=["GET", "POST"])
def home():
    caption = None
    image_url = None

    if request.method == "POST":
        image = request.files["image"]
        style = request.form.get("style")

        img = Image.open(image).convert("RGB")
        inputs = processor(img, return_tensors="pt")
        output = model.generate(**inputs)
        raw_caption = processor.decode(output[0], skip_special_tokens=True)

        caption = style_caption(raw_caption, style)
        image_url = image.filename

        img.save(f"static/{image.filename}")

    return render_template("index.html", caption=caption, image=image_url)

if __name__ == "__main__":
    app.run(debug=True)
