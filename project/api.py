from openai import OpenAI
from flask import request, jsonify, Blueprint
import os
from project.models import User
from project import db
import json

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
        'error': 'Missing required parameter: text'
      }

    return jsonify({
      'data': json.loads(get_completion(create_prompt(text)))
    })
  except Exception as e:
    print(e)
    return {
      'error': 'Uknown error occured. Please try again later.'
    }
 
    
client = OpenAI()
    
# give instructions to llm on how to complete the task based on the text provided
def create_prompt(text):
  prompt = f"""
    You will be provided with text delimited by triple backticks.
    Your task is to provide input fields for a form described in the text.
    Provide an array of objects in json format with the following keys:
    label, name, and type
    
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

OPEN_AI_DUMMY_RESPONSE = [
        {
            "label": "Name",
            "name": "name",
            "type": "text"
        },
        {
            "label": "Email",
            "name": "email",
            "type": "email"
        },
        {
            "label": "Password",
            "name": "password",
            "type": "password"
        },
        {
            "label": "Confirm Password",
            "name": "confirmPassword",
            "type": "password"
        },
        {
            "label": "Date of Birth",
            "name": "dob",
            "type": "date"
        },
        {
            "label": "Gender",
            "name": "gender",
            "type": "radio"
        },
        {
            "label": "Agree to Terms and Conditions",
            "name": "agree",
            "type": "checkbox"
        },
        {
            "label": "Submit",
            "name": "submit",
            "type": "submit"
        }
]

#
# user endpoints
#

@api.route("/api/v1/users", methods=["GET"])
def get_users():
  try:
    users = User.query.all()

    return jsonify({
      'data': [{
        'id': user.id,
        'username': user.username,
        'email': user.email
      } for user in users]
    })
  except Exception as e:
    print(e)
    return {
      'error': 'Unknown error occured. Please try again later.'
    }, 500

@api.route("/api/v1/user", methods=["POST"])
def create_user():
  try:
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    
    if not username:
      return jsonify({
        'error': 'Missing required parameter: username'
      }), 400
    
    if not email:
      return jsonify({
        'error': 'Missing required parameter: email'
      }), 400
    
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
      'data': {
        'id': user.id,
        'username': user.username,
        'email': user.email
      }
    })
  except Exception as e:
    print(e)
    db.session.rollback()
    return {
      'error': 'Uknown error occured. Please try again later.'
    }, 500