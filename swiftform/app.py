from flask import Flask, jsonify

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    # todo: settings not working atm, need to propery configure env variables
    # app.config.from_object("config.settings")

    # if settings_override:
    #     app.config.update(settings_override)

    # Define a route for the API
    @app.route('/', methods=['GET'])
    def index():
        # You can return any data structure that jsonify can handle.
        return jsonify({"message": "Welcome to my API!"})

    return app










