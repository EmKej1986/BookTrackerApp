from passlib.hash import sha256_crypt
from __init__ import DB

book_identifier = DB.Table('book_identifier', DB.Column('User_id', DB.Integer, DB.ForeignKey('User.id')),
                           DB.Column('Book_id', DB.Integer, DB.ForeignKey('Book.id')))


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    nickname = DB.Column(DB.String(50), unique=True)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password = DB.Column(DB.String(32), nullable=False)
    user_profile = DB.Column(DB.Integer, DB.ForeignKey('UserProfile.id'))

    def __init__(self, nickname, email, password):
        hashed_password = sha256_crypt.hash(password)
        self.username, self.email, self.password = nickname, email, hashed_password


class UserProfile(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.relationship('User', uselist=False, backref='UserProfile')
    books = DB.relationship('Book', secondary=book_identifier)


class Book(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), unique=True, nullable=False)
