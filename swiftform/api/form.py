from flask import Blueprint, request, jsonify, abort
from swiftform.models import Form
from swiftform.app import db
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from swiftform.decorators import require_fields

form = Blueprint("form", __name__)


@form.route("/api/v1/forms", methods=["POST"])
@jwt_required()
@require_fields(["name"])
def create_form():
    data = request.json
    name = data.get("name")
    description = data.get("description", "")

    if len(name) < 2:
        abort(422, description="Form name must be at least 2 characters long")

    try:
        new_form = Form(name=name, description=description, user_id=current_user.id)

        db.session.add(new_form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "id": form.id,
            "name": form.name,
            "description": form.description,
            "user_id": form.user_id,
            "created_at": form.created_at,
            "updated_at": form.updated_at,
        }
    ), 200


@form.route("/api/v1/forms/<int:form_id>", methods=["GET"])
@jwt_required()
def get_form(form_id):
    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        abort(401, description="You are not authorized to view this form")

    return jsonify(
        {
            "id": form.id,
            "name": form.name,
            "description": form.description,
            "user_id": form.user_id,
            "created_at": form.created_at,
            "updated_at": form.updated_at,
        }
    ), 200


@form.route("/api/v1/forms/<int:form_id>", methods=["PUT"])
@jwt_required()
@require_fields(["name"])
def update_form(form_id):
    data = request.json
    name = data.get("name")
    description = data.get("description", "")

    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        abort(401, description="You are not authorized to update this form")

    try:
        if len(name) < 2:
            abort(422, description="Form name must be at least 2 characters long")

        form.name = data.get("name")

        if description:
            form.description = description

        form.updated_at = datetime.now()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "id": form.id,
            "name": form.name,
            "description": form.description,
            "user_id": form.user_id,
        }
    ), 200


@form.route("/api/v1/forms/<int:form_id>", methods=["DELETE"])
@jwt_required()
def delete_form(form_id):
    try:
        form = Form.query.get(form_id)
    except Exception as e:
        raise e

    if form is None:
        abort(404, description="Form not found")

    if form.user_id != current_user.id:
        abort(401, description="You are not authorized to delete this form")

    try:
        db.session.delete(form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Form deleted successfully"}), 200
