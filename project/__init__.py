from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

load_dotenv()  # load environment variables from .env.

def create_app():
  app = Flask(__name__)

  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

  db.init_app(app)

  from .api import api
  app.register_blueprint(api)

  return app


   