from functools import lru_cache

from transformers import BlipForConditionalGeneration, BlipProcessor
from PIL import Image

MODEL_NAME = "Salesforce/blip-image-captioning-base"


@lru_cache(maxsize=1)
def load_model():
    """Load BLIP once, on first use, instead of during application import."""
    processor = BlipProcessor.from_pretrained(MODEL_NAME)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    return processor, model

def generate_caption(image_file):
    processor, model = load_model()
    image = Image.open(image_file).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
