from swiftform.api import api
from openai import OpenAI
from flask import request, jsonify, abort, current_app
import json
from flask_jwt_extended import jwt_required


@api.route("prompt", methods=["POST"])
@jwt_required()
def generate_prompt():
    try:
        text = request.json.get("text", None)

        if not text:
            abort(400, description="Missing required parameter: text")

        openai_enabled = current_app.config.get("OPEN_AI_ENABLED", False)
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

        return jsonify({"data": serialized_openai_response})

    except Exception as e:
        raise e


client = OpenAI()


# give instructions to llm on how to complete the task based on the text provided
def create_prompt(text):
    prompt = f"""
    You are an AI assistant for a form creation tool. You will provide developers with a JSON representation of a form based on the text they provide.

    The text is delimited by triple backticks. In this text, the developer will tell what the form will be used for. The text may not be as detailed as you would like, so you will need to figure it out yourself.

    The form will contain the following properties:
    - name: The name of the form.
    - description: The description of the form.
    - sections: An array of sections in the form.

    Each section should contain the following properties:
    - title: The title of the section.
    - questions: An array of questions in the section.

    Each question should contain the following properties:
    - type: The type of the question.
    - prompt: The prompt for the question.
    - order: The order of the question in the section.
    - validations: An array of validation rules for the question.
    - choices: An array of choices for the question (only for multiple_choice, checkbox, dropdown types).

    Supported questions types are:
    - textfield: A single-line text field.
    - textarea: A multi-line text field.
    - multiple_choice: A multiple-choice question.
    - checkbox: A checkbox question.
    - dropdown: A dropdown question.
    - date: A date picker.

    Each choice should contain the following properties:
    - text: The label for the choice.
    - order: The order of the choice.

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
# prompt = create_prompt("Registration Form")
OPEN_AI_DUMMY_RESPONSE = {
    "description": "A form for users to register for an event.",
    "name": "Registration Form",
    "sections": [
        {
            "questions": [
                {
                    "order": 1,
                    "prompt": "Enter your full name",
                    "type": "textfield",
                    "validations": [
                        {
                            "message": "Please enter your full name",
                            "type": "required",
                            "value": True,
                        }
                    ],
                },
                {
                    "order": 2,
                    "prompt": "Enter your email address",
                    "type": "textfield",
                    "validations": [
                        {
                            "message": "Please enter your email address",
                            "type": "required",
                            "value": True,
                        },
                        {
                            "message": "Please enter a valid email address",
                            "type": "pattern",
                            "value": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                        },
                    ],
                },
                {"order": 3, "prompt": "Select your date of birth", "type": "date"},
            ],
            "title": "Personal Information",
        },
        {
            "questions": [
                {
                    "choices": [
                        {"order": 1, "text": "English"},
                        {"order": 2, "text": "Spanish"},
                        {"order": 3, "text": "French"},
                    ],
                    "order": 1,
                    "prompt": "Select your preferred language",
                    "type": "multiple_choice",
                },
                {
                    "choices": [
                        {"order": 1, "text": "Sports"},
                        {"order": 2, "text": "Music"},
                        {"order": 3, "text": "Travel"},
                    ],
                    "order": 2,
                    "prompt": "Select your interests",
                    "type": "checkbox",
                },
            ],
            "title": "Preferences",
        },
    ],
}
