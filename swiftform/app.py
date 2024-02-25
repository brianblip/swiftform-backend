from flask import Flask
from swiftform.config import Config
from swiftform.database import db
from flask_alembic import Alembic
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from swiftform.api import api

config = Config()
alembic = Alembic()
jwt = JWTManager()


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    alembic.init_app(app)
    CORS(app, support_credentials=True)
    jwt.init_app(app)

    app.register_blueprint(api)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(config.HOST, config.PORT)
