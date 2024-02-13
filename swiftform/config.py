import os
from swiftform.utils import strtobool
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG_SERVER_NAME = os.getenv("SERVER_NAME", "localhost:5000")
PRODUCTION_SERVER_NAME = (
    "{0}:{1}".format(
        os.getenv("FLASK_HOST", "localhost"), os.getenv("FLASK_PORT", "8000")
    ),
)


class Config(object):
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "The Meaning of Life")

    DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

    SERVER_NAME = DEBUG_SERVER_NAME if DEBUG else PRODUCTION_SERVER_NAME

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    OPEN_AI_ENABLED = os.getenv("OPEN_AI_ENABLED", "false") == "true"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    if OPEN_AI_ENABLED and not OPENAI_API_KEY:
        raise Exception("Error: OpenAI API key not configured.")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            os.getenv("POSTGRES_USER", "sfuser"),
            os.getenv("POSTGRES_PASSWORD", "password"),
            os.getenv("POSTGRES_HOST", "swiftform_app"),
            os.getenv("POSTGRES_PORT", 5432),
            os.getenv("POSTGRES_DB", "db_swiftform"),
        ),
    )

    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
