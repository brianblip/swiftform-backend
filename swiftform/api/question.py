from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from datetime import datetime
from swiftform.models import Question, Section
from swiftform.app import db
from swiftform.decorators import require_fields

question = Blueprint("question", __name__)


@question.route("/api/v1/questions", methods=["POST"])
@jwt_required()
@require_fields(["type", "prompt", "section_id", "order"])
def create_question():
    data = request.json
    type = data.get("type")
    prompt = data.get("prompt")
    section_id = data.get("section_id")
    order = data.get("order")

    if len(prompt) < 2:
        abort(422, description="Question prompt must be at least 2 characters long")

    try:
        section = Section.query.get(section_id)

        if section is None:
            abort(404, description="Section not found")
    except Exception as e:
        raise e

    try:
        new_question = Question(
            type=type,
            prompt=prompt,
            section_id=section_id,
            order=order,
            is_required=data.get("is_required", False),
        )

        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": new_question.serialize()}), 201


@question.route("/api/v1/questions/<int:question_id>", methods=["GET"])
@jwt_required()
def get_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
    except Exception as e:
        raise e

    return jsonify({"data": question.serialize()}), 200


@question.route("/api/v1/questions/<int:question_id>", methods=["PUT"])
@jwt_required()
@require_fields(["type", "prompt"])
def update_question(question_id):
    data = request.json
    prompt = data.get("prompt")

    if len(prompt) < 2:
        abort(400, description="Question prompt must be at least 2 characters long")

    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
    except Exception as e:
        raise e

    section_id = data.get("section_id")

    try:
        section = Section.query.get(section_id)
    except Exception as e:
        db.session.rollback()
        raise e
    if section is None:
        abort(404, description="Section not found")

    question.type = data["type"]
    question.prompt = data["prompt"]
    question.section_id = section_id
    question.is_required = data.get("is_required", False)
    question.updated_at = datetime.now()

    db.session.commit()

    return jsonify({"data": question.serialize()}), 200


@question.route("/api/v1/questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
    except Exception as e:
        raise e

    try:
        db.session.delete(question)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Question deleted successfully"}), 200
