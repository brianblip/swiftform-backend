from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from swiftform.error_handlers import handle_exception, handle_bad_request, handle_unauthorized

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("swiftform.config.Config")
    
    db.init_app(app)
    jwt.init_app(app)

    from swiftform.api.auth import auth
    app.register_blueprint(auth)

    from swiftform.api.users import users
    app.register_blueprint(users)

    from swiftform.api.form import form
    app.register_blueprint(form)

    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)

    # Define a route for the API
    @app.route('/', methods=['GET'])
    def index():
        # You can return any data structure that jsonify can handle.
        return jsonify({"message": "Welcome to my API!"})

    return app
