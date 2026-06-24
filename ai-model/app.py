from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import numpy as np
import cv2
import traceback
import gc
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.status_code = 200
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

print("==============================")
print(" STARTING SIGNATUREGUARD API ")
print("==============================")

# ✅ Load TFLite model (uses ~10x less RAM than full TensorFlow)
try:
    import tensorflow as tf
    print("Loading TFLite model...")
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("TFLITE MODEL LOADED SUCCESSFULLY")
    print("INPUT DETAILS:", input_details)
    print("OUTPUT DETAILS:", output_details)
except Exception as e:
    print("MODEL LOADING ERROR")
    traceback.print_exc()
    raise e

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def preprocess_image(image_path):
    print("\n--- PREPROCESS START ---")
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("OpenCV failed to read image")
    print("Original shape:", img.shape)
    img = cv2.resize(img, (128, 128))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    print("Final input shape:", img.shape)
    print("--- PREPROCESS END ---\n")
    return img


@app.route("/")
def home():
    return jsonify({"message": "SignatureGuard API Running", "model": "tflite loaded"})

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

@app.route("/ping")
def ping():
    return jsonify({"success": True})


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        response = make_response()
        response.status_code = 200
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    try:
        print("\n==============================")
        print(" NEW PREDICTION REQUEST ")
        print("==============================")

        file = None
        if "image" in request.files:
            file = request.files["image"]
        elif "file" in request.files:
            file = request.files["file"]
        elif "signature" in request.files:
            file = request.files["signature"]

        if file is None:
            return jsonify({"error": "No image received"}), 400

        filename = secure_filename(file.filename)
        if filename == "":
            filename = "uploaded_image.png"

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print("Saved:", filepath)

        # Preprocess
        image = preprocess_image(filepath)

        # ✅ TFLite inference - uses very little RAM
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        print("RAW OUTPUT:", prediction)
        score = float(prediction[0][0])
        print("SCORE:", score)

        gc.collect()  # free RAM

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



