from swiftform.api import api
from flask import request, jsonify
from swiftform.models import Form, Section, Question, QuestionType
from swiftform.app import db
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from werkzeug.exceptions import Unauthorized, NotFound
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required, MinLength


@api.route("forms", methods=["GET"])
@jwt_required()
def get_forms():
    try:
        try:
            forms = Form.query.filter_by(user_id=current_user.id).all()
        except Exception as e:
            raise e

        return jsonify({"data": [form.serialize() for form in forms]}), 200
    except Exception as e:
        raise e


@api.route("forms", methods=["POST"])
@jwt_required()
def create_form():
    try:
        validate([Required("name"), MinLength("name", 2)])
    except ValidationRuleErrors as e:
        raise e

    name = request.json.get("name")
    description = request.json.get("description", "")

    try:
        new_form = Form(name=name, description=description, user_id=current_user.id)

        db.session.add(new_form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": new_form.serialize()}), 201


@api.route("/forms/nested", methods=["POST"])
@jwt_required()
def create_nested_form():
    form_name = request.json.get("name")
    form_description = request.json.get("description")

    try:
        new_form = Form(
            name=form_name, description=form_description, user_id=current_user.id
        )
        db.session.add(new_form)
        db.session.flush()

        sections = request.json.get("sections")
        for section in sections:
            new_section = Section(title=section["title"], form_id=new_form.id)
            db.session.add(new_section)
            db.session.flush()

            questions = section["questions"]
            for question in questions:
                validations = (
                    question["validations"] if "validations" in question else []
                )

                # check if question has a validation with type "required"
                required_validation = next(
                    (
                        validation
                        for validation in validations
                        if validation["type"] == "required"
                    ),
                    None,
                )

                question_type = QuestionType(question["type"])

                try:
                    new_question = Question(
                        order=question["order"],
                        prompt=question["prompt"],
                        type=question_type,
                        section_id=new_section.id,
                        is_required=required_validation is not None,
                    )

                    db.session.add(new_question)
                except Exception as e:
                    raise e

        db.session.commit()

        return jsonify({"data": new_form.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        raise e


@api.route("forms/<int:form_id>", methods=["GET"])
@jwt_required()
def get_form(form_id):
    try:
        form = Form.query.get(form_id)
        if form is None:
            raise NotFound()
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        raise Unauthorized()

    return jsonify({"data": form.serialize()}), 200


@api.route("forms/<int:form_id>", methods=["PUT"])
@jwt_required()
def update_form(form_id):
    try:
        validate([Required("name"), MinLength("name", 2)])
    except ValidationRuleErrors as e:
        raise e

    description = request.json.get("description", "")

    try:
        form = Form.query.get(form_id)
        if form is None:
            raise NotFound()
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        raise Unauthorized()

    try:
        form.name = request.json.get("name")

        if description:
            form.description = description

        form.updated_at = datetime.now()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": form.serialize()}), 200


@api.route("forms/<int:form_id>", methods=["DELETE"])
@jwt_required()
def delete_form(form_id):
    try:
        form = Form.query.get(form_id)
        if form is None:
            raise NotFound()
    except Exception as e:
        raise e

    if form.user_id != current_user.id:
        raise Unauthorized()

    try:
        db.session.delete(form)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"message": "Form deleted successfully"}), 200
