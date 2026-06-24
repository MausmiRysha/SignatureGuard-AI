from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
import numpy as np
import cv2
import traceback
from werkzeug.utils import secure_filename


app = Flask(__name__)

# ✅ CORS - most aggressive setup
CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     supports_credentials=False
)


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response


@app.after_request
def after_request(response):
    return add_cors_headers(response)


# ✅ Global OPTIONS handler - catches ALL preflight requests
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.status_code = 200
        return add_cors_headers(response)


print("==============================")
print(" STARTING SIGNATUREGUARD API ")
print("==============================")


# Load model
try:
    print("Loading model...")
    model = tf.keras.models.load_model("model.h5")
    print("MODEL LOADED SUCCESSFULLY")
    print("INPUT SHAPE:", model.input_shape)
    print("OUTPUT SHAPE:", model.output_shape)

except Exception as e:
    print("MODEL LOADING ERROR")
    traceback.print_exc()
    raise e


UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def preprocess_image(image_path):
    print("\n--- PREPROCESS START ---")
    print("Image path:", image_path)

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if img is None:
        raise Exception("OpenCV failed to read image")

    print("Original shape:", img.shape)
    img = cv2.resize(img, (128, 128))
    print("After resize:", img.shape)

    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    print("Final model input:", img.shape)
    print("--- PREPROCESS END ---\n")

    return img


@app.route("/")
def home():
    return jsonify({
        "message": "SignatureGuard API Running",
        "model": "loaded"
    })


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


@app.route("/ping")
def ping():
    return jsonify({"success": True})


@app.route("/predict", methods=["POST", "OPTIONS", "GET"])
def predict():

    if request.method == "OPTIONS":
        response = make_response()
        response.status_code = 200
        return add_cors_headers(response)

    if request.method == "GET":
        return jsonify({"message": "predict endpoint alive"})

    try:
        print("\n==============================")
        print(" NEW PREDICTION REQUEST ")
        print("==============================")

        file = None

        if "image" in request.files:
            file = request.files["image"]
            print("Using key: image")
        elif "file" in request.files:
            file = request.files["file"]
            print("Using key: file")
        elif "signature" in request.files:
            file = request.files["signature"]
            print("Using key: signature")

        if file is None:
            print("NO FILE FOUND")
            return jsonify({"error": "No image received"}), 400

        print("Filename:", file.filename)
        filename = secure_filename(file.filename)

        if filename == "":
            filename = "uploaded_image.png"

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print("Saved file:", filepath)

        image = preprocess_image(filepath)

        print("Running TensorFlow prediction...")
        prediction = model.predict(image)
        print("RAW OUTPUT:", prediction)

        score = float(prediction[0][0])
        print("SCORE:", score)

        if score >= 0.5:
            label = "Genuine"
            confidence = score * 100
        else:
            label = "Forged"
            confidence = (1 - score) * 100

        response_data = {
            "prediction": label,
            "status": label,
            "result": label,
            "confidence": round(confidence, 2),
            "raw_score": round(score, 4),
            "image": filename
        }

        print("FINAL RESPONSE:", response_data)
        return jsonify(response_data)

    except Exception as e:
        print("\n*** ERROR ***")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



