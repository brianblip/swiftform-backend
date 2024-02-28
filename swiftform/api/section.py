from swiftform.api import api
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from swiftform.app import db
from swiftform.models import Section, Form
from swiftform.decorators import require_fields


@api.route("sections", methods=["POST"])
@jwt_required()
@require_fields(["title", "form_id"])
def create_section():
    title = request.json.get("title")
    form_id = request.json.get("form_id")

    try:
        form = Form.query.get(form_id)
        if form is None:
            abort(404, description="Form not found")
    except Exception as e:
        db.session.rollback()
        raise e

    if form.user_id != current_user.id:
        abort(401, description="You are not the owner of this form")

    try:
        new_section = Section(title=title, form_id=form_id)

        db.session.add(new_section)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"data": new_section.serialize()}), 201


@api.route("sections/<int:section_id>", methods=["GET"])
@jwt_required()
def get_section(section_id):
    try:
        section = Section.query.get(section_id)
        if section is None:
            abort(404, description="Section not found")
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": section.serialize()}), 200


@api.route("sections/<int:section_id>", methods=["PUT"])
@jwt_required()
def update_section(section_id):
    try:
        section = Section.query.get(section_id)
        if section is None:
            abort(404, description="Section not found")
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e

    section.title = request.json.get("title")
    db.session.commit()

    return jsonify({"data": section.serialize()}), 200


@api.route("sections/<int:section_id>", methods=["DELETE"])
@jwt_required()
def delete_section(section_id):
    try:
        section = Section.query.get(section_id)
        if section is None:
            abort(404, description="Section not found")
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            abort(401, description="You are not the owner of this form")
    except Exception as e:
        db.session.rollback()
        raise e
    try:
        db.session.delete(section)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Section deleted"}), 200
