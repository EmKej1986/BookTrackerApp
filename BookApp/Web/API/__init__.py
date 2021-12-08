from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from BookApp.Web.modelSQL import User

db = SQLAlchemy()
ma = Marshmallow()
user_model = User


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        r'sqlite:///C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.db'

    from views import get_all_user_books_blueprint
    app.register_blueprint(get_all_user_books_blueprint)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    # app.run(debug=True)
    # app.run(host='127.0.0.1', port=5001)


# TODO połączyć z database.sqlite3
# TODO uruchomić API na 5001
