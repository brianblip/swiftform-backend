from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from swiftform.app import db
from swiftform.models import Choice, Question
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required
from werkzeug.exceptions import NotFound


@api.route("choices", methods=["POST"])
@jwt_required()
def create_choice():
    try:
        validate([Required("text"), Required("question_id"), Required("order")])
    except ValidationRuleErrors as e:
        raise e

    text = request.json.get("text")
    question_id = request.json.get("question_id")
    order = request.json.get("order")

    try:
        question = Question.query.get(question_id)
        if question is None:
            raise NotFound()
    except Exception as e:
        db.session.rollback()
        raise e

    try:
        new_choice = Choice(text=text, question_id=question_id, order=order)

        db.session.add(new_choice)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"data": new_choice.serialize()}), 201


@api.route("choices/<int:choice_id>", methods=["GET"])
@jwt_required()
def get_choice(choice_id):
    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            raise NotFound()
    except Exception as e:
        raise e

    return jsonify({"data": choice.serialize()}), 200


@api.route("choices/<int:choice_id>", methods=["PUT"])
@jwt_required()
def update_choice(choice_id):
    try:
        validate([Required("text")])
    except ValidationRuleErrors as e:
        raise e

    text = request.json.get("text")
    order = request.json.get("order")

    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        choice.text = text
        choice.order = order
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"data": choice.serialize()}), 200


@api.route("choices/<int:choice_id>", methods=["DELETE"])
@jwt_required()
def delete_choice(choice_id):
    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        db.session.delete(choice)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"message": "Choice deleted"}), 200
