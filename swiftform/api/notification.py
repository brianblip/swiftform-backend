from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.models import Notification
from swiftform.app import db
from swiftform.validation.validation import ValidationRuleErrors, validate
from swiftform.validation.rules import Required


@api.route("notifications", methods=["POST"])
@jwt_required()
def create_notification():
    try:
        validate([Required("title"), Required("message")])
    except ValidationRuleErrors as e:
        raise e

    title = request.json["title"]
    message = request.json["message"]

    try:
        new_notification = Notification(
            title=title, message=message, recipient_id=current_user.id
        )

        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": new_notification.serialize()}), 201


@api.route("notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    try:
        notifications = Notification.query.filter_by(recipient_id=current_user.id).all()
    except Exception as e:
        raise e

    notification_list = [notification.serialize() for notification in notifications]

    return jsonify({"data": notification_list}), 200
