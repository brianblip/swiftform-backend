from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

class Base(DeclarativeBase):
  pass

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """

    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("swiftform.config.Config")

    db = SQLAlchemy(model_class=Base)
    db.init_app(app)

    # todo: settings not working atm, need to propery configure env variables
    # app.config.from_object("config.settings")

    # if settings_override:
    #     app.config.update(settings_override)

    # Define a route for the API
    @app.route('/', methods=['GET'])
    def index():
        # You can return any data structure that jsonify can handle.
        return jsonify({"message": "Welcome to my API!"})

    return app
