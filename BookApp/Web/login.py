from flask import render_template, redirect, url_for, Blueprint, flash, session
from .forms import RegistrationForm, LoginFrom
from .modelSQL import User, UserProfile
from . import DB
from flask_login import login_user, login_required
from passlib.hash import sha256_crypt

login_blueprint = Blueprint('login', __name__)
book_track_blueprint = Blueprint('book_track', __name__)
create_account_blueprint = Blueprint('logout', __name__)


@login_blueprint.route('/', methods=['POST', 'GET'])
@login_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and sha256_crypt.verify(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session.update({'nickname': form.nickname.data})
            return redirect(url_for('book_track.book_track'))
        else:
            flash('Login Unsuccessful. Please check nickname or password', 'danger')

    return render_template('login.html', title='Login', form=form)


@create_account_blueprint.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = RegistrationForm()
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
    return render_template('create_account.html', title='Sign In', form=form)


@book_track_blueprint.route('/book_track', methods=['GET'])
@login_required
def book_track():
    return redirect('book_track.book_track')

