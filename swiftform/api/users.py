from flask import Blueprint, jsonify

from flask_jwt_extended import jwt_required, current_user

users = Blueprint('users', __name__)




@users.route("/api/v1/users/me", methods=["GET"])
@jwt_required()
def get_currently_logged_in_user():
    return jsonify({
      'data': {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'avatar_url': current_user.avatar_url
      }
    })
    
    