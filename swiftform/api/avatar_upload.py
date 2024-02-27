import os
from swiftform.api import api
from flask import jsonify, request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_jwt_extended import jwt_required, get_jwt_identity
from swiftform.app import db
from swiftform.models import User


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "public")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()  # Get the user's ID from the JWT
    current_user = User.query.get(user_id)  # Fetch the user from the database

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return jsonify({"error": "File already exists"}), 409
        try:
            file.save(file_path)
            current_user.avatar_url = f"/public/{filename}"
            db.session.commit()

        except OSError:
            return jsonify(
                {"error": "Unexpected error occurred while saving the file"}
            ), 500

        return jsonify({"success": "File successfully uploaded"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@api.route("upload", methods=["PATCH"])
@jwt_required()
def update_file():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if current_user.avatar_url:
            old_file_path = os.path.join(BASE_DIR, current_user.avatar_url.lstrip("/"))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        if os.path.exists(file_path):
            return jsonify({"error": "File already exists"}), 409

        try:
            file.save(file_path)
            current_user.avatar_url = f"/public/{filename}"
            db.session.commit()

        except OSError:
            return jsonify(
                {"error": "Unexpected error occurred while saving the file"}
            ), 500

        return jsonify({"success": "File successfully updated"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@api.route("upload", methods=["DELETE"])
def delete_file():
    filename = request.json.get("filename")
    if filename is None:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": "File successfully deleted"}), 200
    else:
        return jsonify({"error": "File not found"}), 404


@api.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(_):
    return jsonify({"error": "File size too large"}), 413
