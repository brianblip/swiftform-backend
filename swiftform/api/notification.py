from swiftform.api import api
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.models import Notification
from swiftform.app import db
from swiftform.decorators import require_fields


@api.route("notifications", methods=["POST"])
@jwt_required()
@require_fields(["title", "message", "recipient_id"])
def create_notification():
    data = request.json
    title = data["title"]
    message = data["message"]

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
        notifications = Notification.query.filter_by(
            recipient_id=current_user.id).all()
    except Exception as e:
        raise e

    notification_list = [notification.serialize()
                         for notification in notifications]

    return jsonify({"data": notification_list}), 200
