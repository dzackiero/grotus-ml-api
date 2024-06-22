from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import io

app = Flask(__name__)

# Load your pre-trained Keras model
model = load_model('model.keras')

def prepare_image(img, target_size):
    # Load image with target size
    img = load_img(img, target_size=target_size)
    # Convert the image to an array
    img = img_to_array(img)
    # Expand the shape of the array
    img = np.expand_dims(img, axis=0)
    # Normalize the image data
    img = img / 255.0
    return img

@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Prepare the image for the model
            img = io.BytesIO(file.read())
            processed_image = prepare_image(img, target_size=(224, 224))  # Change target_size based on your model

            # Make a prediction
            predictions = model.predict(processed_image)

            # Assuming your model has specific classes it predicts
            response = {}
            if predictions[0][0] > 0.7:
                response["prediction"] = "Full Nutrition"
            elif predictions[0][1] > 0.7:
                response["prediction"] = "Lack of Potassium"
            elif predictions[0][2] > 0.7:
                response["prediction"] = "Lack of Nitrogen"
            else:
                response["prediction"] = "Lack of Red Phosphor"

            response["predictions"] = predictions.tolist()

            return jsonify(response)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
