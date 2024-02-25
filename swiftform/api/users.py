from swiftform.api import api
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user


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
