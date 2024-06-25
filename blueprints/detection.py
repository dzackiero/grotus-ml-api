from flask import Blueprint, request, jsonify
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import io

model = load_model("model/model.keras")
bp = Blueprint("detection", __name__)


def prepare_image(img, target_size):
    img = load_img(img, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img


@bp.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Prepare the image for the model
            img = io.BytesIO(file.read())
            processed_image = prepare_image(
                img, target_size=(224, 224)
            )  # Change target_size based on your model

            # Make a prediction
            predictions = model.predict(processed_image)

            # Assuming your model has specific classes it predicts
            response = {}
            if predictions[0][0] > 0.7:
                response["prediction"] = "Full Nutrition"
                response["keyword"] = None
            elif predictions[0][1] > 0.7:
                response["prediction"] = "Lack of Potassium"
                response["keyword"] = "Pottasium"
            elif predictions[0][2] > 0.7:
                response["prediction"] = "Lack of Nitrogen"
                response["keyword"] = "Nitrogen"
            elif predictions[0][3] > 0.7:
                response["prediction"] = "Lack of Red Phosphor"
                response["keyword"] = "Phosphorus"
            else:
                response["prediction"] = (
                    "Couldn't Detect Lack of Nutrition from the image"
                )
                response["keyword"] = None

            response["predictions"] = predictions.tolist()

            return jsonify(response)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid request"}), 400
