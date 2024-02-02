from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from swiftform.app import db
from swiftform.models import Section, Form

section = Blueprint("section", __name__)


@section.route("/api/v1/sections", methods=["POST"])
@jwt_required()
def create_section():
    data = request.json

    form_id = data.get("form_id")
    # Get the form from the database
    form = Form.query.get(form_id)

    # Check if the form exists and the current user is the creator of the form
    if not form or form.user_id != current_user.id:
        abort(
            404, description="You are not authorized to create a section in this form"
        )

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

    form = Form.query.get(section.form_id)
    if form.user_id != current_user.id:
        abort(403, description="You are not authorized to view this section")

    section_data = {
        "id": section.id,
        "title": section.title,
        "form_id": section.form_id,
    }

    return jsonify(section_data)
