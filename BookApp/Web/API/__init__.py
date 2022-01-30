from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        r'sqlite:///C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.sqlite3'

    CORS(app)
    from views import get_all_user_books_blueprint
    app.register_blueprint(get_all_user_books_blueprint)

    db.init_app(app)
    ma.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run(host='0.0.0.0', port=5001)