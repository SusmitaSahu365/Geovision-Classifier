from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
from model_loader import model  # ✅ already loads the model safely

app = Flask(__name__)
app.secret_key = "deploy_secret_key"  # optional here

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page — upload form
@app.route("/")
def home():
    return render_template("upload.html")

# Upload + prediction
@app.route("/uploads", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"})

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type"})

    filename = secure_filename(file.filename)

    upload_dir = os.path.join("static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    # Preprocess image
    img = load_img(file_path, target_size=(255, 255))
    img_array = img_to_array(img) / 255.0
    img_array = np.reshape(img_array, (1, 255, 255, 3))

    # Predict
    predictions = model.predict(img_array)
    class_names = ["Cloudy", "Desert", "Green_Area", "Water"]
    predicted_label = class_names[np.argmax(predictions)]

    return jsonify({
        "success": True,
        "prediction": predicted_label,
        "image_path": file_path
    })

if __name__ == "__main__":
    # For Render, use host 0.0.0.0 and dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
