from swiftform.api import api
from flask import jsonify, request
from swiftform.models import Answer, Question
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required
from swiftform.app import db


@api.route("answers", methods=["POST"])
@jwt_required()
def create_answer():
    try:
        validate([Required("response_id"), Required("question_id"), Required("text")])
    except ValidationRuleErrors as e:
        raise e

    response_id = request.json.get("response_id")
    question_id = request.json.get("question_id")
    text = request.json.get("text")
    try:
        question = Question.query.get(question_id)
        if question is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        answer = Answer(response_id=response_id, question_id=question_id, text=text)

        db.session.add(answer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": answer.serialize()}), 201


@api.route("answers/<int:answer_id>", methods=["GET"])
@jwt_required()
def get_answer(answer_id):
    try:
        answer = Answer.query.get(answer_id)
        if answer is None:
            raise NotFound()
    except Exception as e:
        raise e

    return jsonify({"data": answer.serialize()}), 200


@api.route("answers/<int:answer_id>", methods=["PUT"])
@jwt_required()
def update_answer(answer_id):
    try:
        validate([Required("text")])
    except ValidationRuleErrors as e:
        raise e

    text = request.json.get("text")
    try:
        answer = Answer.query.get(answer_id)
        if answer is None:
            raise NotFound()
    except Exception as e:
        raise e

    answer.text = text
    db.session.commit()

    return jsonify({"data": answer.serialize()}), 200


@api.route("answers/<int:answer_id>", methods=["DELETE"])
@jwt_required()
def delete_answer(answer_id):
    try:
        answer = Answer.query.get(answer_id)
        if answer is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        db.session.delete(answer)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify({"message": "Answer deleted successfully"}), 200
