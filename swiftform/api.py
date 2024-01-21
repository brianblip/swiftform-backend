from flask import Blueprint, request, jsonify, abort
from swiftform.models import User
from swiftform.app import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user

api = Blueprint('api', __name__)



# ========== AUTH ENDPOINTS ==========




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

@api.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
      user = User.query.filter_by(email=email).first()

      if not user or not check_password_hash(user.password, password):
        abort(401, description='Invalid email or password')
    except Exception as e:
      raise e
       
    try:
        access_token = create_access_token(identity=user)
    except Exception as e:
        raise e

    return jsonify({'data': {'access_token': access_token}})




# ========== USER ENDPOINTS ==========




@api.route("/api/v1/users/me", methods=["GET"])
@jwt_required()
def get_currently_logged_inuser():
    return jsonify({
      'data': {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'avatar_url': current_user.avatar_url
      }
    })
    
    