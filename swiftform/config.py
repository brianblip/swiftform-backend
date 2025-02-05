import os
from swiftform.utils import strtobool
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "The Meaning of Life")

    ENV = os.getenv("FLASK_ENV", "development")

    DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

    HOST = os.getenv("FLASK_HOST", "localhost")

    PORT = os.getenv("FLASK_PORT", "8000")

    SERVER_NAME = os.getenv("SERVER_NAME", "{0}:{1}".format(HOST, PORT))

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

    MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH', 8_388_608)

    JWT_COOKIE_SECURE = ENV == "production"
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # todo: this should be True in production
    JWT_COOKIE_CSRF_PROTECT = ENV == "production"
