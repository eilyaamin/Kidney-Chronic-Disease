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
        model = Preprocessor()
        columns = model.get_columns()
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


@models_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        model_name = data.get('model')
        if not model_name:
            return jsonify({"error": "Missing 'model' in request data"}), 400

        model_instance = None
        model_classes = {
            "Random Forest": RandomForest,
            "Decision Tree": DecisionTree,
            "XGBoost": XGBoost,
            "Gradient Boosting": GradientBoosting
        }

        if model_name in model_classes:
            model_instance = model_classes[model_name]()
        else:
            return (
                jsonify({"error": "Invalid model name. Expected RandomForest, DecisionTree, XGBoost, or GradientBoosting"}),
                400,
            )

        data.pop('model', None)  # Remove 'model' key from data

        preprocessor = Preprocessor()
        features = preprocessor.get_data().drop("classification", axis=1).columns.tolist()
        keys_list = list(data.keys())

        values = []
        for feature in features:
            feature_word = preprocessor.translate_token_to_word(feature)
            if feature_word in keys_list:
                feature_value = data[feature_word]
                values.append({feature: feature_value})

        data_dict = {key: [d[key]] for d in values for key in d}
        values_df = pd.DataFrame(data_dict)

 
        # preprocessed_data = values_df
        preprocessed_data = preprocessor.preprocess_new_record(values_df)
        if preprocessed_data is not None:
            predictions = model_instance.predict(preprocessed_data)
            print(predictions)
        else:
            print("Preprocessing failed.")

        return jsonify({"predictions": predictions}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500