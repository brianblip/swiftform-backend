from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from swiftform.models import Notification
from swiftform.app import db

notification = Blueprint("notification", __name__)


@notification.route("/api/v1/notifications", methods=["POST"])
@jwt_required()
def create_notification():
    data = request.json

    try:
        new_notification = Notification(
            title=data["title"], message=data["message"], recipient_id=current_user.id
        )

        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return jsonify({"data": new_notification.serialize()}), 201


@notification.route("/api/v1/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    try:
        notifications = Notification.query.filter_by(recipient_id=current_user.id).all()
    except Exception as e:
        raise e

    notification_list = [notification.serialize() for notification in notifications]

    return jsonify({"data": notification_list}), 200
