import tensorflow as tf
import numpy as np


model = tf.keras.models.load_model("model.h5")

print("Input shape:")
print(model.input_shape)

print("Output shape:")
print(model.output_shape)

print("\nModel Summary:")

model.summary()


x = np.zeros(
    (1,128,128,1),
    dtype="float32"
)


print("\nTesting prediction...")


result = model.predict(x)


print("Result:")

print(result)