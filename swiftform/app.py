from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("swiftform.config.Config")
    
    db = SQLAlchemy(model_class=Base)
    db.init_app(app)

    # Define a route for the API
    @app.route('/', methods=['GET'])
    def index():
        # You can return any data structure that jsonify can handle.
        return jsonify({"message": "Welcome to my API!"})

    return app
