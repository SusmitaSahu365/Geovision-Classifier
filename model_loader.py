from keras.models import load_model
import os

MODEL_PATH = os.path.join("model", "Modelmain.h5")

print("✅ Loading model once...")
model = load_model(MODEL_PATH)

