from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
import traceback


app = Flask(__name__)

CORS(app)



print("Loading model...")


model = tf.keras.models.load_model(
    "model.h5"
)


print("MODEL LOADED SUCCESSFULLY")


print(
    "MODEL INPUT:",
    model.input_shape
)


print(
    "MODEL OUTPUT:",
    model.output_shape
)





def preprocess_image(path):


    print(
        "Reading image:",
        path
    )


    img = cv2.imread(

        path,

        cv2.IMREAD_COLOR

    )


    if img is None:

        raise Exception(
            "Image reading failed"
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
        "Resize shape:",
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


    return img







@app.route("/")
def home():

    return jsonify({

        "message":
        "SignatureGuard API Running"

    })







@app.route(
    "/predict",
    methods=["POST"]
)

def predict():


    try:


        print("\n====================")

        print("NEW PREDICTION REQUEST")

        print("====================")



        print(
            "FILES:",
            request.files
        )



        if "image" not in request.files:


            return jsonify({

                "error":
                "No image received"

            }),400




        file = request.files["image"]



        print(
            "FILE NAME:",
            file.filename
        )



        if not os.path.exists("uploads"):

            os.makedirs(
                "uploads"
            )



        filepath = os.path.join(

            "uploads",

            file.filename

        )



        file.save(filepath)



        print(
            "IMAGE SAVED:",
            filepath
        )



        image = preprocess_image(

            filepath

        )



        print(
            "Running model..."
        )



        prediction = model.predict(

            image

        )



        print(
            "RAW MODEL OUTPUT:",
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


            result = "Genuine"

            confidence = score * 100



        else:


            result = "Forged"

            confidence = (1-score) * 100




        response = {


            "status":

            result,


            "confidence":

            round(
                confidence,
                2
            ),


            "raw_score":

            round(
                score,
                4
            ),


            "image":

            file.filename

        }



        print(
            "FINAL RESPONSE:",
            response
        )



        return jsonify(response)





    except Exception as e:


        print(
            "ERROR OCCURRED"
        )


        traceback.print_exc()



        return jsonify({

            "error":
            str(e)

        }),500






if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )