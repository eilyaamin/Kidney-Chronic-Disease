from ml import ChronicDiseasePredictor
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    """endpoint to evaluate patient chronic kidney disease situation"""
    try:
        data = request.json

        # Validate the input data
        if not isinstance(data, list):
            return (
                jsonify({"error": "Invalid input format. Expected a list of records."}),
                400,
            )

        patient_data = pd.DataFrame(data)
        model = ChronicDiseasePredictor()

        # Validate the input columns
        if set(patient_data.columns) != set(model.columns):
            return (
                jsonify(
                    {
                        "error": "Invalid input columns. Expected: {}".format(
                            list(model.columns)
                        )
                    }
                ),
                400,
            )

        predictions = model.predict(patient_data)
        return jsonify({"predictions": predictions.tolist()}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500
