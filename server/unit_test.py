"""Unit tests for the Flask API."""
import unittest
import json
from json.decoder import JSONDecodeError
from flask import Flask
import requests
from ml import ChronicDiseasePredictor


class FlaskAPITestCase(unittest.TestCase):
    """Flask API unit test case"""

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.predictor = ChronicDiseasePredictor()

    def test_predict_endpoint_valid_input(self):
        """test for valid input"""
        data = [
            {
                "Bp": 50,
                "Sg": 1.02,
                "Al": 4,
                "Su": 1,
                "Rbc": 1,
                "Bu": 18,
                "Sc": 0.8,
                "Sod": 137.53,
                "Pot": 4.63,
                "Hemo": 11.3,
                "Wbcc": 6000,
                "Rbcc": 4.71,
                "Htn": 1,
            }
        ]

        try:
            headers = {"Content-Type": "application/json"}
            timeout = 5  # Specify the timeout value in seconds
            response = requests.post(
                "http://localhost:5000/predict",
                data=json.dumps(data),
                headers=headers,
                timeout=timeout,
            )

            self.assertEqual(response.status_code, 200)
            response_data = response.json()  # Retrieve the response content as JSON
            predictions = response_data["predictions"]
            self.assertTrue(
                predictions[0] in [0, 1]
            )  # Check if the predicted value is 0 or 1

        except JSONDecodeError:
            self.fail("Invalid JSON response received.")


    def test_predict_endpoint_invalid_columns(self):
        """test for invalid columns"""
        data = [
            {
                "Bp": 50,
                "Sg": 1.02,
                "InvalidColumn": 4,  # Invalid column name
                "Su": 1,
                "Rbc": 1,
            }
        ]

        try:
            headers = {"Content-Type": "application/json"}
            timeout = 5  # Specify the timeout value in seconds
            response = requests.post(
                "http://localhost:5000/predict",
                data=json.dumps(data),
                headers=headers,
                timeout=timeout,
            )

            self.assertEqual(response.status_code, 400)
            response_data = response.json()  # Retrieve the response content as JSON
            self.assertIn("Invalid input columns", response_data["error"])

        except JSONDecodeError:
            self.fail("Invalid JSON response received.")
