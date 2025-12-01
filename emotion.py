import threading
import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .config import HF_EMOTION_MODEL

tokenizer = None
model = None
loaded = False

def _load_model_background():
    global tokenizer, model, loaded
    try:
        print("🧠 Loading emotion model in background...")
        tokenizer = AutoTokenizer.from_pretrained(HF_EMOTION_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(HF_EMOTION_MODEL)
        loaded = True
        print("✅ Emotion model loaded successfully!")
    except Exception as e:
        print("❌ Failed to load emotion model:", e)

# Start background thread
threading.Thread(target=_load_model_background, daemon=True).start()

def detect_emotion(text):
    if not loaded:
        # model still loading
        return "loading", 0.0

    encoded = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        out = model(**encoded)
    scores = torch.softmax(out.logits, dim=1)[0]
    idx = torch.argmax(scores).item()
    label = model.config.id2label[idx]
    return label, scores[idx].item()
