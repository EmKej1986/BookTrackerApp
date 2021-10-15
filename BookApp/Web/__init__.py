from flask_sqlalchemy import SQLAlchemy
from flask import Flask

DB = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///database.sqlite3'
    DB.init_app(app)
    return app

