import importlib
import os

from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api/v1")


# Import all API routes in this module
api_routes = [f for f in os.listdir(os.path.dirname(
    os.path.abspath(__file__))) if f.endswith(".py") and f != "__init__.py"]

for api_route in api_routes:
    importlib.import_module(os.path.dirname(
        os.path.realpath(__file__)).split('/')[-1] + "." + api_route[:-3])


@api.route("/")
def index():
    return "API is OK!"
