from flask import Flask
from swiftform.config import Config
from swiftform.database import db
from swiftform.jwt_manager import jwt
from flask_alembic import Alembic
from flask_cors import CORS
from swiftform.api import api
from swiftform.error_handlers import ExceptionHandlers

config = Config()
alembic = Alembic()


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

    app.register_error_handler(Exception,
                               ExceptionHandlers.handle_exception)
    app.register_error_handler(400,
                               ExceptionHandlers.handle_bad_request)
    app.register_error_handler(401,
                               ExceptionHandlers.handle_unauthorized)
    app.register_error_handler(404,
                               ExceptionHandlers.handle_not_found)
    app.register_error_handler(422,
                               ExceptionHandlers.handle_unprocessable_content)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(config.HOST, config.PORT)
