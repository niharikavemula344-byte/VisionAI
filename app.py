import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request
from PIL import UnidentifiedImageError

from caption import generate_caption

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
UPLOAD_FOLDER = Path(app.static_folder) / "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def style_caption(caption, style):
    if style == "funny":
        return f"😂 {caption} — looks like it’s having a great day!"
    if style == "dramatic":
        return f"🎭 In a world of silence… {caption}."
    else:  # professional
        return caption

@app.route("/", methods=["GET", "POST"])
def home():
    caption = None
    image_url = None

    if request.method == "POST":
        image = request.files.get("image")
        style = request.form.get("style", "professional")
        suffix = Path(image.filename if image else "").suffix.lower()

        if not image or not image.filename or suffix not in ALLOWED_EXTENSIONS:
            return render_template("index.html", error="Choose a JPG, PNG, or WebP image."), 400

        try:
            UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
            filename = f"{uuid4().hex}{suffix}"
            destination = UPLOAD_FOLDER / filename
            image.save(destination)
            raw_caption = generate_caption(destination)
            caption = style_caption(raw_caption, style)
            image_url = f"uploads/{filename}"
        except (UnidentifiedImageError, OSError):
            return render_template("index.html", error="The uploaded file is not a valid image."), 400

    return render_template("index.html", caption=caption, image=image_url)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
