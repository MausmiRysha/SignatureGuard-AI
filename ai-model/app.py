from flask import Flask, request, jsonify
from flask_cors import CORS
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
import numpy as np
import cv2
import os
import traceback
from werkzeug.utils import secure_filename


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


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


    img = cv2.imread(
        image_path,
        cv2.IMREAD_COLOR
    )


    if img is None:

        raise Exception(
            "OpenCV failed to read image"
        )


    print(
        "Original shape:",
        img.shape
    )


    img = cv2.resize(
        img,
        (128,128)
    )


    print(
        "After resize:",
        img.shape
    )


    img = img.astype(
        "float32"
    ) / 255.0



    img = np.expand_dims(
        img,
        axis=0
    )


    print(
        "Final model input:",
        img.shape
    )


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

    return jsonify({

        "status":"OK"

    })






@app.route("/predict", methods=["POST"])
def predict():

    try:

        print("\n\n==============================")
        print(" NEW PREDICTION REQUEST ")
        print("==============================")


        print(
            "Headers:",
            request.headers
        )


        print(
            "Files received:",
            request.files
        )


        print(
            "Form data:",
            request.form
        )



        file = None


        # Accept different frontend keys

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

            return jsonify({

                "error":
                "No image received"

            }),400





        print(
            "Filename:",
            file.filename
        )


        filename = secure_filename(
            file.filename
        )


        if filename == "":

            filename = "uploaded_image.png"



        filepath = os.path.join(

            UPLOAD_FOLDER,

            filename

        )



        file.save(filepath)



        print(
            "Saved file:",
            filepath
        )




        # Preprocess

        image = preprocess_image(
            filepath
        )



        print(
            "Running TensorFlow prediction..."
        )


        prediction = model.predict(
            image
        )



        print(
            "RAW OUTPUT:",
            prediction
        )



        score = float(
            prediction[0][0]
        )



        print(
            "SCORE:",
            score
        )



        if score >= 0.5:

            label = "Genuine"

            confidence = score * 100


        else:

            label = "Forged"

            confidence = (1-score) * 100





        response = {

            "prediction": label,

            "status": label,

            "result": label,

            "confidence": round(
                confidence,
                2
            ),

            "raw_score": round(
                score,
                4
            ),

            "image": filename

        }



        print(
            "FINAL RESPONSE:"
        )

        print(response)



        return jsonify(response)





    except Exception as e:


        print("\n******** ERROR ********")


        traceback.print_exc()


        return jsonify({

            "error": str(e)

        }),500






if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000

    )
