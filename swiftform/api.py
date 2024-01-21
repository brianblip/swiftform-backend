from flask import Blueprint, request, jsonify, abort
from swiftform.models import User
from swiftform.app import db

from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

api = Blueprint('api', __name__)

@api.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    avatar_url = request.json.get('avatar_url')

    try:
        user = User.query.filter_by(email=email).first()

        if user:
            abort(400, description='User already exists')

    except Exception as e:
        raise e

    try:
      hashed_password = generate_password_hash(password, method="scrypt")
    except Exception as e:
      raise e
        
    try:  
      new_user = User(name=name, email=email, password=hashed_password, avatar_url=avatar_url)
      db.session.add(new_user)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e

    try:
      access_token = create_access_token(identity=new_user)
    except Exception as e:
      raise e

    return jsonify({
        'data': {
            'access_token': access_token,
        }
    })
    
    