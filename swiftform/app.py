from flask import Flask
from swiftform.config import Config
from swiftform.database import db
from swiftform.jwt_manager import jwt, refresh_expiring_token
from flask_alembic import Alembic
from flask_cors import CORS
from swiftform.api import api
from swiftform.exception_handlers import ExceptionHandlers

config = Config()
alembic = Alembic()
exception_handlers = ExceptionHandlers()


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__, static_folder="public", static_url_path="/public")
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    alembic.init_app(app)
    CORS(app, supports_credentials=True)
    jwt.init_app(app)
    exception_handlers.init_app(app)

    app.register_blueprint(api)

    app.after_request(refresh_expiring_token)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(config.HOST, config.PORT)
