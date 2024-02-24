from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    set_access_cookies,
    current_user,
)
from swiftform.error_handlers import (
    handle_exception,
    handle_bad_request,
    handle_unauthorized,
    handle_not_found,
    handle_unprocessable_content,
)
from flask_cors import CORS
from datetime import timedelta, datetime, timezone


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
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8MB
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)

    # Using an `after_request` callback, we refresh any token that is within 30 minutes of expiring.
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=current_user)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    from swiftform.api.auth import auth

    app.register_blueprint(auth)

    from swiftform.api.users import users

    app.register_blueprint(users)

    from swiftform.api.form import form

    app.register_blueprint(form)

    from swiftform.api.section import section

    app.register_blueprint(section)

    from swiftform.api.question import question

    app.register_blueprint(question)
    from swiftform.api.response import response

    app.register_blueprint(response)

    from swiftform.api.prompt import prompt

    app.register_blueprint(prompt)

    from swiftform.api.answer import answer

    app.register_blueprint(answer)

    from swiftform.api.notification import notification

    app.register_blueprint(notification)

    from swiftform.api.choice import choice

    app.register_blueprint(choice)

    from swiftform.api.avatar_upload import avatar_upload

    app.register_blueprint(avatar_upload)

    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(422, handle_unprocessable_content)

    return app
