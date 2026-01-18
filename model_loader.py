import os
import subprocess
from keras.models import load_model

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "Modelmain.h5")
FILE_ID = "1fBQdulES8JMWcm-SDbCxvkHZ58pLGqU_"

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Skip download if file already exists
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
        print("✅ Model already exists, skipping download")
        return

    print("📥 Downloading model from Google Drive...")
    cmd = [
        "python", "-m", "gdown",
        "--id", FILE_ID,
        "--fuzzy",
        "-O", MODEL_PATH
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("❌ Model download failed:", e)
        raise e

    size = os.path.getsize(MODEL_PATH)
    print(f"⬇️ Downloaded model size: {size / (1024*1024):.2f} MB")

# Load the model **once** at import
_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        download_model()
        print("✅ Loading model into memory...")
        _model_instance = load_model(MODEL_PATH)
    return _model_instance

# Load immediately on import
model = get_model()
