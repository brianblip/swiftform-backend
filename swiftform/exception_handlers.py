from flask import jsonify
from swiftform.validation.validation import ValidationRuleErrors
from werkzeug.exceptions import Unauthorized, NotFound


def on_validation_error(e: ValidationRuleErrors):
    errors = []
    for error in e.error_bags:
        errors.append({"field": error.attribute, "message": error.description})

    return jsonify({"message": errors[0]["message"], "errors": errors})


def on_unauthorized_error(e: Unauthorized):
    return jsonify({"message": "Unauthorized"})


def on_not_found_error(e: NotFound):
    return jsonify({"message": "Not Found"})


def on_exception(e):
    return jsonify({"message": str(e)}), 500


class ExceptionHandlers(object):
    def init_app(self, app):
        app.register_error_handler(Exception, on_exception)
        app.register_error_handler(ValidationRuleErrors, on_validation_error)
        app.register_error_handler(Unauthorized, on_unauthorized_error)
        app.register_error_handler(NotFound, on_not_found_error)
