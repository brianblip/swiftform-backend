from flask import Flask
from swiftform.config import Config
from flask_alembic import Alembic

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
    alembic.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(config.HOST, config.PORT)
