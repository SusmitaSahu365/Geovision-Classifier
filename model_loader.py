import os
import subprocess
from keras.models import load_model

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "Modelmain.h5")
FILE_ID = "1fBQdulES8JMWcm-SDbCxvkHZ58pLGqU_"

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Remove corrupted file if exists
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)

    cmd = [
        "python", "-m", "gdown",
        "--id", FILE_ID,
        "--fuzzy",
        "-O", MODEL_PATH
    ]

    subprocess.run(cmd, check=True)

    size = os.path.getsize(MODEL_PATH)
    print(f"⬇️ Downloaded model size: {size / (1024*1024):.2f} MB")

def get_model():
    if not os.path.exists(MODEL_PATH):
        print("📥 Downloading model from Google Drive...")
        download_model()

    print("✅ Loading model...")
    return load_model(MODEL_PATH)

model = get_model()
