from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.app import db
from swiftform.models import Section, Form
from werkzeug.exceptions import Unauthorized, NotFound
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required


@api.route("sections", methods=["POST"])
@jwt_required()
def create_section():
    try:
        validate([Required("title"), Required("form_id")])
    except ValidationRuleErrors as e:
        raise e

    title = request.json.get("title")
    form_id = request.json.get("form_id")
    order = request.json.get("order")

    try:
        form = Form.query.get(form_id)
        if form is None:
            raise NotFound()
    except Exception as e:
        db.session.rollback()
        raise e

    if form.user_id != current_user.id:
        raise Unauthorized()

    try:
        new_section = Section(title=title, form_id=form_id, order=order)

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
            raise NotFound()
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            raise Unauthorized()
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
            raise NotFound()
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            raise Unauthorized()
    except Exception as e:
        db.session.rollback()
        raise e

    section.title = request.json.get("title")
    section.order = request.json.get("order")
    db.session.commit()

    return jsonify({"data": section.serialize()}), 200


@api.route("sections/<int:section_id>", methods=["DELETE"])
@jwt_required()
def delete_section(section_id):
    try:
        section = Section.query.get(section_id)
        if section is None:
            raise NotFound()
    except Exception as e:
        raise e

    try:
        form = Form.query.get(section.form_id)
        if form.user_id != current_user.id:
            raise Unauthorized()
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
