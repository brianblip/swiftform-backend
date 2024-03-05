import importlib
import os

from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api/v1")


import swiftform.api.answer
import swiftform.api.auth
import swiftform.api.avatar_upload
import swiftform.api.choice
import swiftform.api.form
import swiftform.api.notification
import swiftform.api.prompt
import swiftform.api.question
import swiftform.api.response
import swiftform.api.section
import swiftform.api.users


@api.route("/")
def index():
    return "API is OK!"