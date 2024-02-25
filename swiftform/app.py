from flask import Flask
from swiftform.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_cors import CORS
from flask_jwt_extended import JWTManager

config = Config()
db = SQLAlchemy()
alembic = Alembic()
jwt = JWTManager()


def load_models():
    """
    Lazy loading models helps prevent circular imports and enables
    Alembic to discover the models effectively.
    """
    from swiftform import models  # noqa: F401


load_models()


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

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(config.HOST, config.PORT)
