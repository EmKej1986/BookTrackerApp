from flask import request, Blueprint, render_template
from __init__ import user_model


get_all_user_books_blueprint = Blueprint('get_books', __name__)


@get_all_user_books_blueprint.route('/get_books', methods=['GET'])  # get_books/?username=Mateusz
def get_all_user_books():
    # username = request.args['username']
    user = user_model.query.get()
    user_books = user.user_profile.books
    # db.session.commit()
    print(user_books)
    return []


get_all_user_books()


    #    {
    #        "available": [book1, book2, ...],
    #        "unavailable": [book3, book4, ...]
    #
    #   }
