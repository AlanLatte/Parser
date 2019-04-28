import os

from flask import Flask, current_app

from app.main import bp

def create_app():
    app = Flask(__name__)
    # app.config.from_object(os.environ['APP_CONFIG'])
    app.register_blueprint(bp)

    return app
