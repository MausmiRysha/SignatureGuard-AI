import tensorflow as tf

# Load your existing model
model = tf.keras.models.load_model("model.h5")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save it
with open("model.tflite", "wb") as f:
    f.write(tflite_model)

print("Done! Check model.tflite size:")
import os
print(os.path.getsize("model.tflite"), "bytes")