from swiftform.api import api
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from swiftform.models import Question, Section
from swiftform.app import db
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required, MinLength
from werkzeug.exceptions import NotFound, Unauthorized


@api.route("questions", methods=["POST"])
@jwt_required()
def create_question():
    try:
        validate(
            [
                Required("type"),
                Required("prompt"),
                Required("section_id"),
                Required("order"),
                MinLength("prompt", 2),
            ]
        )
    except ValidationRuleErrors as e:
        raise e

    type = request.json.get("type")
    prompt = request.json.get("prompt")
    section_id = request.json.get("section_id")
    order = request.json.get("order")

    try:
        section = Section.query.get(section_id)
        if section is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        if section.form.user_id != current_user.id:
            raise Unauthorized()
    except Exception as e:
        raise e

    try:
        new_question = Question(
            type=type,
            prompt=prompt,
            section_id=section_id,
            order=order,
            is_required=request.json.get("is_required", False),
        )

        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": new_question.serialize()}), 201


@api.route("questions/<int:question_id>", methods=["GET"])
@jwt_required()
def get_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            raise NotFound()
    except Exception as e:
        raise e
    try:
        if question.section.form.user_id != current_user.id:
            raise Unauthorized()
    except Exception as e:
        raise e

    return jsonify({"data": question.serialize()}), 200


@api.route("questions/<int:question_id>", methods=["PUT"])
@jwt_required()
def update_question(question_id):
    try:
        validate(
            [
                Required("type"),
                Required("prompt"),
                Required("section_id"),
                MinLength("prompt", 2),
            ]
        )
    except ValidationRuleErrors as e:
        raise e
    try:
        question = Question.query.get(question_id)
        if question is None:
            raise NotFound()
    except Exception as e:
        raise e

    section_id = request.json.get("section_id")

    try:
        section = Section.query.get(section_id)
    except Exception as e:
        db.session.rollback()
        raise e
    if section is None:
        raise NotFound()

    try:
        question.section.form.user_id != current_user.id
    except Exception as e:
        raise e

    question.type = request.json["type"]
    question.prompt = request.json["prompt"]
    question.section_id = section_id
    question.is_required = request.json.get("is_required", False)
    question.updated_at = datetime.now()
    question.order = request.json.get("order")

    db.session.commit()

    return jsonify({"data": question.serialize()}), 200


@api.route("questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        question = Question.query.get(question_id)
        if question.section.form.user_id != current_user.id:
            raise Unauthorized()
    except Exception as e:
        raise e

    try:
        db.session.delete(question)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Question deleted successfully"}), 200
