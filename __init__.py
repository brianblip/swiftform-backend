from flask import Flask
from dotenv import load_dotenv
from .api import api

load_dotenv()  # load environment variables from .env.

def create_app():
  app = Flask(__name__)
  app.register_blueprint(api)

  return app


   