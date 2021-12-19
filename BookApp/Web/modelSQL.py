from passlib.hash import sha256_crypt
from . import DB, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


book_identifier = DB.Table('book_identifier', DB.Model.metadata,
                           DB.Column('UserProfile_id', DB.ForeignKey('UserProfile.id')),
                           DB.Column('Book_id', DB.ForeignKey('Book.id')))


class User(DB.Model, UserMixin):
    __tablename__ = 'User'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(50), unique=True)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password = DB.Column(DB.String(32), nullable=False)
    user_profile = DB.Column(DB.Integer, DB.ForeignKey('UserProfile.id'))

    def __init__(self, username, email, password, user_profile):
        hashed_password = sha256_crypt.hash(password)
        self.username, self.email, self.password, self.user_profile = username, email, hashed_password, user_profile

    def __str__(self):
        return f"{self.username} {self.email}"


class UserProfile(DB.Model):
    __tablename__ = 'UserProfile'
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.relationship('User', uselist=False, backref='UserProfile')
    books = DB.relationship('Book', secondary=book_identifier)


class Book(DB.Model):
    __tablename__ = 'Book'
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), nullable=False)
    url = DB.Column(DB.String(500), nullable=True)
    is_available = DB.Column(DB.Boolean, default=False)

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title
