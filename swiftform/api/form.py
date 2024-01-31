from flask import Blueprint, request, jsonify, abort
from swiftform.models import Form
from swiftform.app import db
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime

form = Blueprint("form", __name__)


@form.route("/api/v1/forms", methods=["POST"])
@jwt_required()
def create_form():
    data = request.json

    # validate minlength of form name
    if len(data.get("name", "")) < 2:
        abort(400, description="Form name must be at least 2 characters long")

    # Get the user ID of the currently logged-in user
    user_id = current_user.id

    try:
        new_form = Form(
            name=data["name"], description=data["description"], user_id=user_id
        )

        db.session.add(new_form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    form_dict = {
        "id": new_form.id,
        "name": new_form.name,
        "description": new_form.description,
        "user_id": new_form.user_id,
        "created_at": new_form.created_at,
        "updated_at": new_form.updated_at,
    }

    return jsonify(form_dict), 201


@form.route("/api/v1/forms/<int:form_id>", methods=["GET"])
@jwt_required()
def get_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        abort(404, description="Form not found")

    user_id = current_user.id

    # Check if the logged-in user is the creator of the form
    if form.user_id != user_id:
        abort(403, description="You are not authorized to view this form")

    form_data = {
        "id": form.id,
        "name": form.name,
        "description": form.description,
        "user_id": form.user_id,
        "created_at": form.created_at,
        "updated_at": form.updated_at,
    }
    return jsonify(form_data), 200


@form.route("/api/v1/forms/<int:form_id>", methods=["PUT"])
@jwt_required()
def update_form(form_id):
    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    user_id = current_user.id

    if form.user_id != user_id:
        abort(403, description="You are not authorized to update this form")

    data = request.json

    try:
        # validate minlength of form name
        if len(data.get("name", form.name)) < 2:
            abort(400, description="Form name must be at least 2 characters long")

        form.name = data.get("name", form.name)
        form.description = data.get("description", form.description)
        form.updated_at = datetime.now()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    form_data = {
        "id": form.id,
        "name": form.name,
        "description": form.description,
        "user_id": form.user_id,
        "updated_at": form.updated_at,
    }
    return jsonify(form_data), 200


@form.route("/api/v1/forms/<int:form_id>", methods=["DELETE"])
@jwt_required()
def delete_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        abort(404, description="Form not found")

    user_id = current_user.id

    if form.user_id != user_id:
        abort(403, description="You are not authorized to delete this form")

    db.session.delete(form)
    db.session.commit()
    return jsonify({"message": "Form deleted successfully"}), 200
