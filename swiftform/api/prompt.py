from swiftform.api import api
from openai import OpenAI
from flask import request, jsonify, abort
import json
import os

from flask_jwt_extended import jwt_required

openai_enabled = os.environ.get("OPENAI_ENABLED", "false").lower() == "true"


@api.route("prompt", methods=["POST"])
@jwt_required()
def generate_prompt():
    try:
        text = request.json.get("text", None)

        if not text:
            abort(400, description="Missing required parameter: text")

        if not openai_enabled:
            return jsonify({"data": OPEN_AI_DUMMY_RESPONSE})

        prompt = create_prompt(text)

        openai_response = get_completion(prompt)

        if not openai_response:
            abort(500, description="Error generating OpenAI response")

        try:
            serialized_openai_response = json.loads(openai_response)
        except json.JSONDecodeError:
            abort(500, description="Error parsing OpenAI response")

        return jsonify({"data": serialized_openai_response.fields})

    except Exception as e:
        raise e


client = OpenAI()


# give instructions to llm on how to complete the task based on the text provided
def create_prompt(text):
    prompt = f"""
    You will be provided with text delimited by triple backticks.
    This text will describe a form that you need to help create.

    Your task is to provide an array of objects in JSON format. Each item in the array should represent a field in the form. Each object should contain the following properties:
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
    response = client.chat.completions.create(
        response_format={
            "type": "json_object",
        },
        model=model,
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content


# dummy response for when openai is disabled
OPEN_AI_DUMMY_RESPONSE = [
    {
        "label": "Username",
        "name": "username",
        "type": "text",
        "validations": [
            {"message": "Username is required", "type": "required", "value": True},
            {
                "message": "Username must be at least 6 characters long",
                "type": "minLength",
                "value": 6,
            },
            {
                "message": "Username cannot exceed 20 characters",
                "type": "maxLength",
                "value": 20,
            },
        ],
    },
    {
        "label": "Email",
        "name": "email",
        "type": "email",
        "validations": [
            {"message": "Email is required", "type": "required", "value": True},
            {
                "message": "Invalid email format",
                "type": "pattern",
                "value": "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
            },
        ],
    },
    {
        "label": "Password",
        "name": "password",
        "type": "password",
        "validations": [
            {"message": "Password is required", "type": "required", "value": True},
            {
                "message": "Password must be at least 8 characters long",
                "type": "minLength",
                "value": 8,
            },
        ],
    },
    {
        "label": "Confirm Password",
        "name": "confirmPassword",
        "type": "password",
        "validations": [
            {
                "message": "Confirm Password is required",
                "type": "required",
                "value": True,
            },
            {
                "message": "Confirm Password must be at least 8 characters long",
                "type": "minLength",
                "value": 8,
            },
        ],
    },
]
