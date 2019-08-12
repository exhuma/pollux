from flask import Flask
from pollux.blueprint.main import MAIN


def make_app():
    app = Flask(__name__)
    app.register_blueprint(MAIN)
    return app
