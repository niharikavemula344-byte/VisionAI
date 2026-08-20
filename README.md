# VisionText AI

VisionText AI started as my experiment with connecting a pretrained vision model to a simple web interface. You can upload an image and the BLIP model will generate a caption. I also added three presentation styles to make the output more fun to explore.

## What I built

- BLIP-powered image captioning
- Three output presentation styles
- Lazy model loading for faster application startup
- Validated file types, randomized filenames, and a 10 MB upload limit
- Responsive browser interface

## Tech stack

- Python 3.9+
- Flask
- Hugging Face Transformers
- PyTorch
- Pillow

## Quick start

```bash
git clone https://github.com/niharikavemula344-byte/VisionAI.git
cd VisionAI
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The first caption request downloads the public BLIP model, so it can take longer than later requests.

## Project structure

```text
.
├── app.py              # Flask routes and upload validation
├── caption.py          # Cached BLIP inference
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    └── index.html
```

## What I learned

Building this helped me learn how model inference fits into a Flask request, why models should be loaded only once, and how uploaded files need to be validated.

## Privacy and limitations

Uploaded files are processed by the local application and saved under `static/uploads`, which is excluded from Git. BLIP captions may be incomplete or inaccurate; do not use them for safety-critical or accessibility decisions without human review.
