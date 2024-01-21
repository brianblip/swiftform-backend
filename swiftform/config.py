import os
from swiftform.utils import strtobool

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'The Meaning of Life')

    DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

    SERVER_NAME = os.getenv(
        "SERVER_NAME", "{0}:{1}".format(os.getenv("FLASK_HOST", "localhost"), os.getenv("FLASK_PORT", "8000"))
    )
