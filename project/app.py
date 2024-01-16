from flask import Flask

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    return app





