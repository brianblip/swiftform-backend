from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime
from swiftform.models import Notification
from swiftform.app import db

notification = Blueprint("notification", __name__)


@notification.route("/api/v1/notifications", methods=["POST"])
@jwt_required()
def create_notification():
    data = request.json

    user_id = current_user.id

    try:
        new_notification = Notification(
            title=data["title"], message=data["message"], recipient_id=user_id
        )

        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    # Convert the new_notification object to a dictionary so it can be returned as JSON
    notification_dict = {
        "id": new_notification.id,
        "recipient_id": new_notification.recipient_id,
        "title": new_notification.title,
        "message": new_notification.message,
    }

    return jsonify(notification_dict), 201


@notification.route("/api/v1/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = current_user.id

    notifications = Notification.query.filter_by(recipient_id=user_id).all()

    notification_list = []
    for notification in notifications:
        notification_list.append(
            {
                "id": notification.id,
                "recipient_id": notification.recipient_id,
                "title": notification.title,
                "message": notification.message,
            }
        )

    return jsonify(notification_list), 200  