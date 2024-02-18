from flask import Blueprint, request, jsonify, abort
from swiftform.models import User
from swiftform.app import db
from swiftform.decorators import require_fields

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    unset_jwt_cookies,
    set_access_cookies,
)

auth = Blueprint("auth", __name__)


@auth.route("/api/v1/auth/register", methods=["POST"])
@require_fields(["name", "email", "password"])
def register_user():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    avatar_url = request.json.get("avatar_url")

    try:
        user = User.query.filter_by(email=email).first()

        if user:
            abort(400, description="User already exists")
    except Exception as e:
        raise e

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


@auth.route("/api/v1/auth/login", methods=["POST"])
@require_fields(["email", "password"])
def login_user():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            abort(401, description="Invalid email or password")
    except Exception as e:
        raise e

    try:
        access_token = create_access_token(identity=user)
    except Exception as e:
        raise e

    response = jsonify({"data": user.serialize()})
    set_access_cookies(response, access_token)

    return response


@auth.route("/api/v1/auth/logout", methods=["POST"])
def logout_user():
    response = jsonify({"message": "Successfully logged out"})

    unset_jwt_cookies(response)

    return response
