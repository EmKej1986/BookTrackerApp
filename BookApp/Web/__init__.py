from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta


DB = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from web.modelSQL import User, UserProfile, Book
    flask_migrate = Migrate()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@db:5432/book_db'
    app.config['SECRET_KEY'] = 'ToyotaCamry'
    app.permanent_session_lifetime = timedelta(minutes=60)
    DB.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    from main import login_blueprint, register_blueprint, book_track_blueprint, add_book_blueprint, logout_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(book_track_blueprint)
    app.register_blueprint(add_book_blueprint)
    app.register_blueprint(logout_blueprint)

    flask_migrate.init_app(app=app, db=DB)

    return app
