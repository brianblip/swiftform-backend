from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required
from swiftform.app import db
from swiftform.models import Choice, Question
from swiftform.decorators import require_fields

choice = Blueprint("choice", __name__)


@choice.route("/api/v1/choices", methods=["POST"])
@jwt_required()
@require_fields(["text", "question_id", "order"])
def create_choice():
    data = request.json
    text = data.get("text")
    question_id = data.get("question_id")
    order = data.get("order")

    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
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


@choice.route("/api/v1/choices/<int:choice_id>", methods=["GET"])
@jwt_required()
def get_choice(choice_id):
    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            abort(404, description="Choice not found")
    except Exception as e:
        raise e

    return jsonify({"data": choice.serialize()}), 200


@choice.route("/api/v1/choices/<int:choice_id>", methods=["PUT"])
@jwt_required()
@require_fields(["text"])
def update_choice(choice_id):
    data = request.json
    text = data.get("text")

    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            abort(404, description="Choice not found")
    except Exception as e:
        raise e

    try:
        choice.text = text
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"data": choice.serialize()}), 200


@choice.route("/api/v1/choices/<int:choice_id>", methods=["DELETE"])
@jwt_required()
def delete_choice(choice_id):
    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            abort(404, description="Choice not found")
    except Exception as e:
        raise e

    try:
        db.session.delete(choice)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"message": "Choice deleted"}), 200
