from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from swiftform.app import db
from swiftform.models import Section, Form

section = Blueprint("section", __name__)


@section.route("/api/v1/sections", methods=["POST"])
@jwt_required()
def create_section():
    data = request.json

    # Chech if user is the owner of the form
    form_id = request.json.get("form_id")
    try:
        form = Form.query.get(form_id)
    except Exception as e:
        db.session.rollback()
        raise e

    if form is None:
        abort(404, description="Form not found")

    if form.user_id != current_user.id:
        abort(401, description="You are not the owner of this form")

    try:
        new_section = Section(title=data["title"], form_id=form_id)

        db.session.add(new_section)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify(
        {
            "id": new_section.id,
            "title": new_section.title,
            "form_id": new_section.form_id,
        }
    ), 201


@section.route("/api/v1/sections/<int:section_id>", methods=["GET"])
@jwt_required()
def get_section(section_id):
    section = Section.query.get(section_id)
    if section is None:
        abort(404, description="Section not found")
    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify(
        {
            "id": section.id,
            "title": section.title,
            "form_id": section.form_id,
        }
    )


@section.route("/api/v1/sections/<int:section_id>", methods=["PUT"])
@jwt_required()
def update_section(section_id):
    data = request.json
    section = Section.query.get(section_id)
    if section is None:
        abort(404, description="Section not found")
    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e

    section.title = data["title"]
    db.session.commit()

    return jsonify(
        {
            "id": section.id,
            "title": section.title,
            "form_id": section.form_id,
        }
    ), 200


@section.route("/api/v1/sections/<int:section_id>", methods=["DELETE"])
@jwt_required()
def delete_section(section_id):
    section = Section.query.get(section_id)
    if section is None:
        abort(404, description="Section not found")
    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e

    db.session.delete(section)
    db.session.commit()

    return jsonify({"message": "Section deleted"}), 200
