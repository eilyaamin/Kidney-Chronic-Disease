from src.models.rf import RandomForest
from src.models.xgb import XGBoost
from src.models.dt import DecisionTree
from src.models.gb import GradientBoosting
from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from src.preprocess import Preprocessor

models_bp = Blueprint("models_bp", __name__)


@models_bp.route("/features", methods=["GET"])
def get_features():
    try:
        model = Preprocessor()  # Create an instance of the Preprocessor class
        columns = model.get_columns()  # Get the list of preprocessed columns/features
        return jsonify(columns), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@models_bp.route("/models", methods=["GET"])
def get_models():

    rf = RandomForest()
    dt = DecisionTree()
    xgb = XGBoost()
    gb = GradientBoosting()
    try:
        models = [
            {"name": rf.name, "description": rf.description, "accuracy": rf.accuracy},
            {"name": dt.name, "description": dt.description, "accuracy": dt.accuracy},
            {"name": xgb.name, "description": xgb.description, "accuracy": xgb.accuracy},
            {"name": gb.name, "description": gb.description, "accuracy": gb.accuracy},
        ]

        return jsonify(models), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# @models_bp.route("/predict/rf", methods=["POST"])  # Change "GET" to "POST"
# def rf_predict():
#     try:
#         data = request.json

#         # Validate the input data
#         if not isinstance(data, list):
#             return (
#                 jsonify({"error": "Invalid input format. Expected a list of records."}),
#                 400,
#             )

#         patient_data = pd.DataFrame(data)

#         model = RandomForest()

#         # Validate the input columns
#         if set(patient_data.columns) != set(model.get_required_features()):  # Update this line
#             return (
#                 jsonify(
#                     {
#                         "error": "Invalid input columns. Expected: {}".format(
#                             model.get_required_features()
#                         )
#                     }
#                 ),
#                 400,
#             )

#         predictions = model.predict(patient_data)
#         return jsonify({"predictions": predictions.tolist()}), 200

#     except Exception as err:
#         return jsonify({"error": str(err)}), 500

