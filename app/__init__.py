import os

from flask import Flask, current_app

from app.main import bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(bp)

    return app
