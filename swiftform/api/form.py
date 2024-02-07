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
    description = data.get("description", "")

    if len(data.get("name", "")) < 2:
        abort(400, description="Form name must be at least 2 characters long")

    try:
        new_form = Form(
            name=data["name"], description=description, user_id=current_user.id
        )

        db.session.add(new_form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "id": new_form.id,
            "name": new_form.name,
            "description": new_form.description,
            "user_id": new_form.user_id,
            "created_at": new_form.created_at,
            "updated_at": new_form.updated_at,
        }
    ), 201


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
        abort(403, description="You are not authorized to view this form")

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
def update_form(form_id):
    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to update this form")

    data = request.json

    try:
        if len(data.get("name", form.name)) < 2:
            abort(400, description="Form name must be at least 2 characters long")

        form.name = data.get("name", form.name)
        form.description = data.get("description", form.description)
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
        abort(403, description="You are not authorized to delete this form")

    try:
        db.session.delete(form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Form deleted successfully"}), 200
