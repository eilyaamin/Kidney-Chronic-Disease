"""This module is used to setup the Flask app.

"""
import os

from flask import Flask
from flask_cors import CORS

from src.routes import models_bp


def create_app():
    """Factory function to setup the Flask app"""
    app = Flask(__name__)
    app.debug = True

    app.register_blueprint(models_bp)

    CORS(app)

    return app
