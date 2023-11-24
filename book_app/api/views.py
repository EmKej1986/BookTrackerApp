from flask import request, Blueprint
from book_app.web.modelSQL import User, UserProfile, Book
import json

get_all_user_books_blueprint = Blueprint('get_books', __name__)


@get_all_user_books_blueprint.route('/get_books', methods=['GET'])
def get_all_user_books():
    username = request.args['username']

    books_json = {"available": [], "unavailable": []}

    user = User.query.filter_by(username=username).first()
    user_id = user.user_profile
    user_profile = UserProfile.query.get(user_id)
    books = user_profile.books

    available_books = Book.query.filter_by(is_available=1).all()

    for book in books:
        book_url = Book.query.filter_by(title=str(book)).first().url
        if book in available_books:
            books_json["available"].append({"title": str(book), "url": book_url})
        else:
            books_json["unavailable"].append({"title": str(book), "url": book_url})

    jsonobj = json.dumps(books_json)
    return jsonobj
