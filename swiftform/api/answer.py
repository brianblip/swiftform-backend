from swiftform.api import api
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required
from swiftform.models import Answer, Question
from swiftform.decorators import require_fields
from swiftform.app import db


@api.route("answers", methods=["POST"])
@jwt_required()
@require_fields(["response_id", "question_id", "text"])
def create_answer():
    response_id = request.json.get("response_id")
    question_id = request.json.get("question_id")
    text = request.json.get("text")

    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404, description="Question not found")
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
            abort(404, description="Answer not found")
    except Exception as e:
        raise e

    return jsonify({"data": answer.serialize()}), 200


@api.route("answers/<int:answer_id>", methods=["PUT"])
@jwt_required()
@require_fields(["text"])
def update_answer(answer_id):
    text = request.json.get("text")

    try:
        answer = Answer.query.get(answer_id)
        if answer is None:
            abort(404, description="Answer not found")
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
            abort(404, description="Answer not found")
    except Exception as e:
        raise e

    try:
        db.session.delete(answer)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify({"message": "Answer deleted successfully"}), 200
