import os
import gdown
from keras.models import load_model

MODEL_PATH = "model/Modelmain.h5"
MODEL_URL = "https://drive.google.com/file/d/1fBQdulES8JMWcm-SDbCxvkHZ58pLGqU_/view?usp=drive_link"

if not os.path.exists(MODEL_PATH):
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

model = load_model(MODEL_PATH)
