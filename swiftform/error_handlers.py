from flask import jsonify


def handle_bad_request(e):
    return jsonify({"message": e.description}), 400


def handle_unauthorized(e):
    return jsonify({"message": e.description}), 401


def handle_unauthorized(e):
  return jsonify({
        "message": e.description
    }), 401

def handle_exception(e):
  return jsonify({
        "message": str(e)
    }), 500

def handle_not_found(e):
  return jsonify({
        "message": e.description
    }), 404
