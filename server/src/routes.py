from src.models.rf import RandomForest 
from src.models.xgb import XGBoost
from src.models.dt import DecisionTree
from src.models.gb import GradientBoosting
from flask import Flask, request, jsonify, Blueprint
import pandas as pd


files_bp = Blueprint("files_bp", __name__)



@files_bp.route("/predict/rf", methods=["POST"])
def rf_predict():
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
        model = RandomForest()

        # Validate the input columns
        # if set(patient_data.columns) != set(model.columns):
        #     return (
        #         jsonify(
        #             {
        #                 "error": "Invalid input columns. Expected: {}".format(
        #                     list(model.columns)
        #                 )
        #             }
        #         ),
        #         400,
        #     )

        predictions = model.predict(patient_data)
        return jsonify({"predictions": predictions.tolist()}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500
