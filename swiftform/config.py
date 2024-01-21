import os
from swiftform.utils import strtobool

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'The Meaning of Life')

    DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

    SERVER_NAME = os.getenv(
        "SERVER_NAME", "{0}:{1}".format(os.getenv("FLASK_HOST", "localhost"), os.getenv("FLASK_PORT", "8000"))
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://{0}:{1}@{2}:{3}/{4}".
        format(
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_PORT"),
            os.getenv("POSTGRES_DB"),
        ),
    )

