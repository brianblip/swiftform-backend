from swiftform.api import api
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required
from swiftform.app import db
from swiftform.models import Choice, Question
from swiftform.decorators import require_fields


@api.route("choices", methods=["POST"])
@jwt_required()
@require_fields(["text", "order", "question_id"])
def create_choice():
    text = request.json.get("text")
    question_id = request.json.get("question_id")
    order = request.json.get("order")

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


@api.route("choices/<int:choice_id>", methods=["GET"])
@jwt_required()
def get_choice(choice_id):
    try:
        choice = Choice.query.get(choice_id)
        if choice is None:
            abort(404, description="Choice not found")
    except Exception as e:
        raise e

    return jsonify({"data": choice.serialize()}), 200


@api.route("choices/<int:choice_id>", methods=["PUT"])
@jwt_required()
@require_fields(["text"])
def update_choice(choice_id):
    text = request.json.get("text")

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


@api.route("choices/<int:choice_id>", methods=["DELETE"])
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
