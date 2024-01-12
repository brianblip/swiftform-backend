from openai import OpenAI
from flask import request, jsonify, Blueprint
import os
from project.models import User, TokenBlocklist
from project import db
import json
from project.utils import handle_api_exception
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user, get_jwt

api = Blueprint('api', __name__)

OPEN_AI_ENABLED = os.getenv('OPEN_AI_ENABLED', 'false') == 'true'

#
# main endpoints
#

@api.route("/api/v1/prompt", methods=["POST"])
def prompt():
  try:
    if not OPEN_AI_ENABLED:
      return {
        'data': OPEN_AI_DUMMY_RESPONSE
      }
    
    text = request.json.get('text', None)

    if not text:
      return {
        'message': 'Missing required parameter: text'
      }, 400

    return jsonify({
      'data': json.loads(get_completion(create_prompt(text)))
    })
  except Exception as e:
    return handle_api_exception(e)
 
if OPEN_AI_ENABLED:
    client = OpenAI()
    
# give instructions to llm on how to complete the task based on the text provided
def create_prompt(text):
  prompt = f"""
    You will be provided with text delimited by triple backticks.
    This text will describe a form that you need to help create.
    Your task is to provide an array of objects in JSON format.
    - label: The label of the field.
    - name: The name attribute of the field.
    - type: The type of the input field (e.g., text, email, password).
    - validations: An array of validation rules for the field.

    Validations are optional. If validations are provided, you must provide an array of validation objects. And it must contain the following properties:
    - type: The type of validation (e.g., required, minLength, maxLength).
    - value: The value of the validation (e.g., true, 10, 100).
    - message: The error message to display if the validation fails.

    Supported validations are:
    - required: The field is required.
    - minLength: The minimum length of the field.
    - maxLength: The maximum length of the field.
    - min: The minimum value of the field.
    - max: The maximum value of the field.
    - pattern: The pattern the field must match.

    ```{text}```
    """
  
  return prompt

# returns the response from llm based on the prompt provided
def get_completion(prompt, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response =  client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0
  )
  
  return response.choices[0].message.content

# dummy response for when openai is disabled
OPEN_AI_DUMMY_RESPONSE = [
        {
            "label": "Username",
            "name": "username",
            "type": "text",
            "validations": [
                {
                    "message": "Username is required",
                    "type": "required",
                    "value": True
                },
                {
                    "message": "Username must be at least 6 characters long",
                    "type": "minLength",
                    "value": 6
                },
                {
                    "message": "Username cannot exceed 20 characters",
                    "type": "maxLength",
                    "value": 20
                }
            ]
        },
        {
            "label": "Email",
            "name": "email",
            "type": "email",
            "validations": [
                {
                    "message": "Email is required",
                    "type": "required",
                    "value": True
                },
                {
                    "message": "Invalid email format",
                    "type": "pattern",
                    "value": "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
                }
            ]
        },
        {
            "label": "Password",
            "name": "password",
            "type": "password",
            "validations": [
                {
                    "message": "Password is required",
                    "type": "required",
                    "value": True
                },
                {
                    "message": "Password must be at least 8 characters long",
                    "type": "minLength",
                    "value": 8
                }
            ]
        },
        {
            "label": "Confirm Password",
            "name": "confirmPassword",
            "type": "password",
            "validations": [
                {
                    "message": "Confirm Password is required",
                    "type": "required",
                    "value": True
                },
                {
                    "message": "Confirm Password must be at least 8 characters long",
                    "type": "minLength",
                    "value": 8
                }
            ]
        }
    ]

#
# user endpoints
#

# get currently logged in user data
@api.route("/api/v1/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
  try:
    # user_id = session.get("user_id")

    # user = User.query.filter_by(id=user_id).first()

    # if not user:
    #   return jsonify({
    #     'message': 'User not found'
    #   })

    return jsonify({
      'data': {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'avatar_url': current_user.avatar_url
      }
    })
  except Exception as e:
    handle_api_exception(e)


#
# auth endpoints
#
    
@api.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    avatar_url = request.json.get('avatar_url')

    try:
        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({
                'message': 'User already exists'
            }), 400
        
        hashed_password = generate_password_hash(password, method="scrypt")

        new_user = User(name=name, email=email, password=hashed_password, avatar_url=avatar_url)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user)

        return jsonify({
            'data': {
                'access_token': access_token,
            }
        })
    
    except Exception as e:
        db.session.rollback()
        handle_api_exception(e)


@api.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({
                'message': 'Invalid email or password'
            }), 401
        
        access_token = create_access_token(identity=user)

        return jsonify({
            'data': {
                'access_token': access_token,
            }
        })

    except Exception as e:
        handle_api_exception(e)


@api.route("/api/v1/auth/logout", methods=["POST"])
@jwt_required()
def logout_user():
    try:
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return jsonify({
            'message': 'Successfully logged out'
        })
    except Exception as e:
        return handle_api_exception(e)
    



