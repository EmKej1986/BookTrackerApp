from book_app.web import create_app, DB
from book_app.web.modelSQL import *

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        DB.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
