from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.models import Response, Form
from swiftform.app import db
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required
from werkzeug.exceptions import Unauthorized, NotFound


@api.route("responses", methods=["POST"])
@jwt_required()
def create_response():
    try:
        validate([Required("form_id")])
    except ValidationRuleErrors as e:
        raise e

    form_id = request.json.get("form_id")

    try:
        form = Form.query.get(form_id)
        if form is None:
            raise NotFound()
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        raise Unauthorized()
    try:
        response = Response(form_id=form_id, user_id=current_user.id)
        db.session.add(response)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "data": response.serialize(),
        }
    ), 201


@api.route("responses", methods=["GET"])
@jwt_required()
def get_responses():
    try:
        responses = Response.query.filter_by(user_id=current_user.id).all()
    except Exception as e:
        raise e

    return jsonify({"data": [response.serialize() for response in responses]}), 200


@api.route("responses/<int:response_id>", methods=["DELETE"])
@jwt_required()
def delete_response(response_id):
    try:
        response = Response.query.get(response_id)
        if response is None:
            raise NotFound()
    except Exception as e:
        raise e

    if response.user_id != current_user.id:
        raise Unauthorized()

    try:
        db.session.delete(response)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Response deleted successfully"}), 200
