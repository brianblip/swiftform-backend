from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.app import db
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required, MinLength
from werkzeug.security import generate_password_hash, check_password_hash
from swiftform.models import User
from werkzeug.exceptions import NotFound


@api.route("users/me", methods=["GET"])
@jwt_required(optional=True)
def get_currently_logged_in_user():
    if not current_user:
        return jsonify({"data": None})
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
    }
    return jsonify({"data": data})


@api.route("users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFound()
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "avatar_url": user.avatar_url,
        }
        return jsonify({"data": data})
    except Exception as e:
        raise e


@api.route("users/me", methods=["PATCH"])
@jwt_required()
def update_user():
    try:
        new_name = request.json.get("name")
        current_password = request.json.get("current_password")
        new_password = request.json.get("new_password")

        if new_name:
            validate([Required("name")])
            current_user.name = new_name

        if current_password and new_password:
            if not check_password_hash(current_user.password, current_password):
                return jsonify({"message": "Current password is incorrect"}), 400
            validate([Required("new_password"), MinLength("new_password", 8)])
            current_user.password = generate_password_hash(
                new_password, method="scrypt"
            )

        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    except ValidationRuleErrors as e:
        raise e
    except Exception as e:
        db.session.rollback()
        raise e
