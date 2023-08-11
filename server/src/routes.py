from src.models.rf import RandomForest
from src.models.xgb import XGBoost
from src.models.dt import DecisionTree
from src.models.gb import GradientBoosting
from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from src.preprocess import Preprocessor

models_bp = Blueprint("models_bp", __name__)

preprocessor = Preprocessor()
rf = RandomForest()
dt = DecisionTree()
xgb = XGBoost()
gb = GradientBoosting()
model_classes = {
    rf.name: RandomForest,
    dt.name: DecisionTree,
    xgb.name: XGBoost,
    gb.name: GradientBoosting,
}


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
    try:
        models = [
            {"name": rf.name, "description": rf.description, "accuracy": rf.accuracy},
            {"name": dt.name, "description": dt.description, "accuracy": dt.accuracy},
            {
                "name": xgb.name,
                "description": xgb.description,
                "accuracy": xgb.accuracy,
            },
            {"name": gb.name, "description": gb.description, "accuracy": gb.accuracy},
        ]

        return jsonify(models), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@models_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        model_name = data.get("model")
        if not model_name:
            return jsonify({"error": "Missing 'model' in request data"}), 400

        if model_name in model_classes:
            model_instance = model_classes[model_name]()
        else:
            return (
                jsonify(
                    {
                        "error": "Invalid model name. Expected RandomForest, DecisionTree, XGBoost, or GradientBoosting"
                    }
                ),
                400,
            )

        data.pop("model", None)  # Remove 'model' key from data

        features = (
            preprocessor.get_data().drop("classification", axis=1).columns.tolist()
        )

        # Create a DataFrame to hold the input values for prediction
        input_data = pd.DataFrame(columns=features)

        # Populate the input_data DataFrame with values from the request data
        for feature in features:
            feature_word = preprocessor.translate_token_to_word(feature)
            if feature_word in data:
                input_data[feature] = [data[feature_word]]

        # Preprocess the input data
        preprocessed_data = preprocessor.preprocess_new_record(input_data)

        if preprocessed_data is not None:
            # Make the prediction
            prediction = model_instance.predict(preprocessed_data).tolist()[0]
            result = {"prediction": prediction}
        else:
            result = {"error": "Preprocessing failed."}

        return jsonify(result)

    except Exception as err:
        print(f"An error occurred: {str(err)}")
