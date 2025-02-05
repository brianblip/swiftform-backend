from swiftform.api import api
from flask import request, jsonify
from swiftform.models import User
from swiftform.app import db
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import (
    Required,
    ValidEmail,
    MinLength,
    UserAlreadyExists,
    ValidCredentials,
)
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    unset_jwt_cookies,
    set_access_cookies,
)


@api.route("auth/register", methods=["POST"])
def register_user():
    try:
        validate(
            [
                Required("name"),
                Required("email"),
                Required("password"),
                MinLength("password", 8),
                UserAlreadyExists("email"),
            ]
        )
        validate([ValidEmail("email")])

    except ValidationRuleErrors as e:
        raise e

    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    avatar_url = request.json.get("avatar_url")

    try:
        hashed_password = generate_password_hash(password, method="scrypt")
    except Exception as e:
        raise e

    try:
        new_user = User(
            name=name, email=email, password=hashed_password, avatar_url=avatar_url
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    try:
        access_token = create_access_token(identity=new_user)
    except Exception as e:
        raise e

    response = jsonify({"data": new_user.serialize()})

    set_access_cookies(response, access_token)
    return response


@api.route("auth/login", methods=["POST"])
def login_user():
    try:
        validate([Required("email"), Required("password")])
        validate([ValidEmail("email")])
        validate([ValidCredentials("email", "password")])
    except ValidationRuleErrors as e:
        raise e

    email = request.json.get("email")

    user = User.query.filter_by(email=email).first()

    try:
        access_token = create_access_token(identity=user)
    except Exception as e:
        raise e

    response = jsonify({"data": user.serialize()})
    set_access_cookies(response, access_token)

    return response


@api.route("auth/logout", methods=["POST"])
def logout_user():
    response = jsonify({"message": "Successfully logged out"})

    unset_jwt_cookies(response)

    return response
