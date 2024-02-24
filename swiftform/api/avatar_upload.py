from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "public")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

avatar_upload = Blueprint("avatar_upload", __name__)


@avatar_upload.route("/upload", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"success": "File successfully uploaded"}), 200


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@avatar_upload.route("/upload", methods=["PATCH"])
def update_file():
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"success": "File successfully uploaded"}), 200


@avatar_upload.route("/upload", methods=["DELETE"])
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
