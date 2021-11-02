from flask import render_template, redirect, url_for, Blueprint, flash, session, request
from .forms import RegistrationForm, LoginForm, AddBookForm
from .modelSQL import User, UserProfile, Book
from . import DB, current_user
from flask_login import login_user, login_required
from passlib.hash import sha256_crypt

login_blueprint = Blueprint('login', __name__)
book_track_blueprint = Blueprint('book_track', __name__)
register_blueprint = Blueprint('register', __name__)
add_book_blueprint = Blueprint('add_book', __name__)


@login_blueprint.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and sha256_crypt.verify(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            session.update({'username': form.username.data})
            return redirect(url_for('book_track.book_track'))
        else:
            flash('Login Unsuccessful. Please check nickname or password', 'danger')

    return render_template('login.html', title='Login', form=form)


@register_blueprint.route('/register', methods=['POST', 'GET'])
def create_account():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        userProfile = UserProfile()
        DB.session.add(userProfile)
        DB.session.commit()
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    user_profile=userProfile.id)
        DB.session.add(user)
        DB.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login.login'))

    return render_template('register.html', title='Register', form=form)


@book_track_blueprint.route('/book_track', methods=['GET'])
@login_required
def book_track():
    return render_template('book_track.html', title='book_track')


@add_book_blueprint.route('/add_book', methods=['POST', 'GET'])
@login_required
def add_book():
    form = AddBookForm(request.form)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            book = Book(title=form.title.data, user_profile=current_user.user_profile)
            DB.session.add(book)
            DB.session.commit()

            return redirect(url_for('book_track.book_track'))

    return render_template('add_book.html', title='Add Book', form=form)
