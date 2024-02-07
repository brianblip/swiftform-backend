from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from swiftform.models import Question, Form, Section
from swiftform.app import db

question = Blueprint("question", __name__)


@question.route("/api/v1/questions", methods=["POST"])
@jwt_required()
def create_question():
    data = request.json

    if len(data.get("prompt", "")) < 2:
        abort(400, description="Question prompt must be at least 2 characters long")

    form_id = data.get("form_id")

    try:
        form = Form.query.get(form_id)
    except Exception as e:
        db.session.rollback()
        raise e

    if form is None:
        abort(404, description="Form not found")

    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to add questions to this form")

    section_id = data.get("section_id")

    try:
        section = Section.query.get(section_id)
    except Exception as e:
        db.session.rollback()
        raise e
    if section is not None and section.form_id != form_id:
        abort(400, description="Section does not belong to the form")

    try:
        new_question = Question(
            form_id=form_id,
            type=data["type"],
            prompt=data["prompt"],
            section_id=section_id,
            is_required=data.get("is_required", False),
        )

        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "id": new_question.id,
            "form_id": new_question.form_id,
            "type": new_question.type.value,
            "prompt": new_question.prompt,
            "section_id": new_question.section_id,
            "is_required": new_question.is_required,
            "min": new_question.min,
            "max": new_question.max,
            "order": new_question.order,
            "steps": new_question.steps,
        }
    ), 201


@question.route("/api/v1/questions/<int:question_id>", methods=["GET"])
@jwt_required()
def get_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
    except Exception as e:
        raise e

    form = Form.query.get(question.form_id)
    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to view this question")

    return jsonify(
        {
            "id": question.id,
            "form_id": question.form_id,
            "type": question.type.value,
            "prompt": question.prompt,
            "section_id": question.section_id,
            "is_required": question.is_required,
            "min": question.min,
            "max": question.max,
            "order": question.order,
            "steps": question.steps,
        }
    ), 200


@question.route("/api/v1/questions/<int:question_id>", methods=["PUT"])
@jwt_required()
def update_question(question_id):
    data = request.json

    if len(data.get("prompt", "")) < 2:
        abort(400, description="Question prompt must be at least 2 characters long")

    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
    except Exception as e:
        raise e

    try:
        form = Form.query.get(question.form_id)
        if form.user_id != current_user.id:
            abort(403, description="You are not authorized to update this question")
    except Exception as e:
        raise e

    section_id = data.get("section_id")

    try:
        section = Section.query.get(section_id)
    except Exception as e:
        db.session.rollback()
        raise e
    if section is not None and section.form_id != question.form_id:
        abort(400, description="Section does not belong to the form")

    question.type = data["type"]
    question.prompt = data["prompt"]
    question.section_id = section_id
    question.is_required = data.get("is_required", False)
    question.updated_at = datetime.now()

    db.session.commit()

    return jsonify(
        {
            "id": question.id,
            "form_id": question.form_id,
            "type": question.type.value,
            "prompt": question.prompt,
            "section_id": question.section_id,
            "is_required": question.is_required,
        }
    ), 200


@question.route("/api/v1/questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        abort(404, description="Question not found")

    form = Form.query.get(question.form_id)
    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to delete this question")

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200
