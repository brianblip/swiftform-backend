from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from swiftform.app import db
import os

users = Blueprint("users", __name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "public")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@users.route("/api/v1/users/me", methods=["GET"])
@jwt_required(optional=True)
def get_currently_logged_in_user():
    if not current_user:
        return jsonify({"data": None})
    data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
    }
    return jsonify({"data": data})


@users.route("/api/v1/users/me", methods=["PUT"])
@jwt_required()
def update_current_user():
    if not current_user:
        return jsonify({"error": "No logged in user"}), 400

    data = request.form

    if "file" in request.files:
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.avatar_url = filename

    if data.get("name"):
        current_user.name = data.get("name")

    if data.get("current_password") and data.get("new_password"):
        if check_password_hash(current_user.password, data["current_password"]):
            new_password = data["new_password"]
            if len(new_password) < 8:
                return jsonify(
                    {"error": "New password must be at least 8 characters long"}
                ), 400
            current_user.password = generate_password_hash(new_password)
        else:
            return jsonify({"error": "Current password is incorrect"}), 400

    # save current_user changes to the database here
    db.session.commit()

    return jsonify({"data": "User updated successfully"})
