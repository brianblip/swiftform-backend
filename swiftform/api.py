from flask import Blueprint, request, jsonify, abort
from swiftform.models import User, TokenBlocklist, Form
from swiftform.app import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from datetime import datetime, timezone

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

@api.route("/api/v1/auth/logout", methods=["POST"])
@jwt_required()
def logout_user():
      jti = get_jwt()["jti"]
      now = datetime.now(timezone.utc)

      try:
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        raise e

      return jsonify({
          'message': 'Successfully logged out'
      })




# ========== USER ENDPOINTS ==========




@api.route("/api/v1/users/me", methods=["GET"])
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


# ========== FORM ==========

@api.route('/api/v1/forms', methods=['POST'])
@jwt_required()
def create_form():
    data = request.json

     # Get the user ID of the currently logged-in user
    user_id = current_user.id

    new_form = Form(
        name=data['name'],
        description=data['description'],
        user_id=user_id,
        created_at=data['created_at'],
        updated_at=data['updated_at']
    )

    db.session.add(new_form)
    db.session.commit()
    return jsonify({'message': 'Form created successfully'}), 201


    



@api.route('/api/v1/forms/<int:form_id>', methods=['GET'])
@jwt_required()
def get_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        return jsonify({'error': 'Form not found'}), 404
    
     # Get the user ID of the currently logged-in user
    user_id = current_user.id

    # Check if the logged-in user is the creator of the form
    if form.user_id != user_id:
        return jsonify({'error': 'You are not authorized to access this form'}), 403
    
    form_data = {
        'id': form.id,
        'name': form.name,
        'description': form.description,
        'user_id': form.user_id,
        'created_at': form.created_at,
        'updated_at': form.updated_at
    }
    return jsonify(form_data), 200



  





    
    