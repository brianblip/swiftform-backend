from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from flask_jwt_extended import JWTManager

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()  # Create the JWTManager instance

load_dotenv()  # load environment variables from .env.

def create_app():
  app = Flask(__name__)

  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
  app.config['SESSION_TYPE'] = 'sqlalchemy'
  app.config['SESSION_SQLALCHEMY'] = db
  app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
  app.config["JWT_SECRET_KEY"] = "asd"  # Change this!

  jwt.init_app(app)
  db.init_app(app)

  from .api import api
  app.register_blueprint(api)

  return app


   