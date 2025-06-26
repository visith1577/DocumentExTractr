import keras  # pyright: ignore[reportMissingTypeStubs]
import numpy as np
import tensorflow as tf  # pyright: ignore[reportMissingTypeStubs]


def load_model():  # pyright: ignore[reportUnknownParameterType]
    model = keras.models.load_model("cnn_doc_classifier.keras")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    return model  # pyright: ignore[reportUnknownVariableType]


def predict_image_class(
    model: keras.Model, image_path: str, img_height: int, img_width: int
):
    img = keras.utils.load_img(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        image_path, target_size=(img_height, img_width)
    )
    img_array = keras.utils.img_to_array(img)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    img_array = tf.expand_dims(  # Create a batch  # pyright: ignore[reportUnknownMemberType, reportAny]
        img_array, 0
    ) 

    predictions = model.predict(img_array)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAny]
    score = tf.nn.softmax(predictions[0])  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]

    class_names = [
        "email",
        "resume",
        "scientific_publication",
    ]  # Assuming this order based on dataset loading
    predicted_class = class_names[np.argmax(score)]  # pyright: ignore[reportUnknownArgumentType]
    confidence = 100 * np.max(score)  # pyright: ignore[reportUnknownArgumentType, reportAny]

    print(
        f"This image most likely belongs to {predicted_class} with a {confidence:.2f}% confidence."
    )
    return predicted_class, confidence
