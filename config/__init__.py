import os

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1")

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "8000"))
)

