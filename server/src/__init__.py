"""This module is used to setup the Flask app.

"""
import os

from flask import Flask
from flask_cors import CORS

from src.routes import files_bp


def create_app():
    """Factory function to setup the Flask app"""
    app = Flask(__name__)

    app.register_blueprint(files_bp)

    CORS(app)

    return app
