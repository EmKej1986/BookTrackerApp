from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from flask_login import LoginManager
from datetime import timedelta

DB = SQLAlchemy()
login_manager = LoginManager()
SHA256 = sha256()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///database.sqlite3'
    app.config['SECRET_KEY'] = 'ToyotaCamry'
    app.permanent_session_lifetime = timedelta(minutes=60)
    DB.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    from .login import login_blueprint, book_track_blueprint, create_account_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(book_track_blueprint)
    app.register_blueprint(create_account_blueprint)

    return app
