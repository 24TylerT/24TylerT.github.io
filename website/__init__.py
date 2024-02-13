from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "databasenew.db"


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'FRC'

  #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{DB_NAME}'
  #stores database in folder
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBtest.db'

  db.init_app(app)

  from .auth import auth
  app.register_blueprint(auth, url_prefix='/')

  from .models import Scout
  with app.app_context():
    db.create_all()

  return app
