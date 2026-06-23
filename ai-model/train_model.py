import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)



IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20


print("==============================")
print(" SIGNATUREGUARD AI TRAINING ")
print("==============================")



# ==============================
# DATA PREPROCESSING
# ==============================


datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,


    rotation_range=25,

    width_shift_range=0.2,

    height_shift_range=0.2,

    zoom_range=0.25,

    shear_range=0.2,

    horizontal_flip=True

)



print("\nLoading training dataset...")



train_generator = datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="training",

    shuffle=True

)



print("\nLoading validation dataset...")



val_generator = datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="validation",

    shuffle=False

)



# ==============================
# DATA DEBUG
# ==============================


print("\n========== DATA DEBUG ==========")


print(
    "Training images:",
    train_generator.samples
)


print(
    "Validation images:",
    val_generator.samples
)



print(
    "Class mapping:"
)


print(
    train_generator.class_indices
)


print(
    "\nExpected:"
)

print(
    "forged = 0"
)

print(
    "genuine = 1"
)



# ==============================
# CNN MODEL
# ==============================


model = Sequential([


    Conv2D(

        32,

        (3,3),

        activation="relu",

        input_shape=(128,128,3)

    ),


    MaxPooling2D(),



    Conv2D(

        64,

        (3,3),

        activation="relu"

    ),


    MaxPooling2D(),



    Conv2D(

        128,

        (3,3),

        activation="relu"

    ),


    MaxPooling2D(),



    Flatten(),



    Dense(

        64,

        activation="relu"

    ),



    Dropout(0.5),



    Dense(

        1,

        activation="sigmoid"

    )

])




print("\n========== MODEL SUMMARY ==========")


model.summary()



# ==============================
# COMPILE
# ==============================


model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)



# ==============================
# CALLBACKS
# ==============================


early_stop = EarlyStopping(

    monitor="val_loss",

    patience=3,

    restore_best_weights=True

)



checkpoint = ModelCheckpoint(

    "model.h5",

    monitor="val_accuracy",

    save_best_only=True,

    mode="max",

    verbose=1

)



# ==============================
# TRAINING
# ==============================


print("\n========== TRAINING START ==========")


history = model.fit(

    train_generator,

    validation_data=val_generator,

    epochs=EPOCHS,

    callbacks=[

        early_stop,

        checkpoint

    ]

)



print("\n========== TRAINING FINISHED ==========")



# ==============================
# TRAINING RESULTS
# ==============================


print("\nFinal Training Accuracy:")

print(

    history.history["accuracy"][-1]

)



print("\nFinal Validation Accuracy:")

print(

    history.history["val_accuracy"][-1]

)



print("\nBest model saved as model.h5")



# ==============================
# TEST PREDICTION
# ==============================


print("\n========== TEST PREDICTION ==========")



images, labels = next(val_generator)



test_image = images[0]


actual_label = labels[0]



test_image = np.expand_dims(

    test_image,

    axis=0

)



prediction = model.predict(

    test_image

)



score = float(

    prediction[0][0]

)



print(

    "Raw prediction:",

    prediction

)



print(

    "Actual label:",

    actual_label

)



print(

    "Score:",

    score

)



if score >= 0.5:

    print(

        "Prediction: GENUINE"

    )

else:

    print(

        "Prediction: FORGED"

    )



print("\n==============================")

print(" TRAINING COMPLETE ")

print("==============================")