from swiftform.api import api
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from swiftform.models import Response, Form
from swiftform.app import db
from swiftform.decorators import require_fields


@api.route("responses", methods=["POST"])
@jwt_required()
@require_fields(["form_id"])
def create_response():
    form_id = request.json.get("form_id")

    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        abort(
            401,
            description="You are not authorized to submit a response for this form",
        )
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
    form_id = request.args.get("form_id")
    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to view responses for this form")

    responses = Response.query.filter_by(form_id=form_id).all()

    response_list = [response.serialize() for response in responses]

    return jsonify({"data": response_list}), 200


@api.route("responses/<int:response_id>", methods=["DELETE"])
@jwt_required()
def delete_response(response_id):
    try:
        response = Response.query.get(response_id)
        if response is None:
            abort(404, description="Response not found")
    except Exception as e:
        raise e

    if response.user_id != current_user.id:
        abort(401, description="You are not authorized to delete this response")

    try:
        db.session.delete(response)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Response deleted successfully"}), 200
