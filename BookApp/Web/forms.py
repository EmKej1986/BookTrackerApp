from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .modelSQL import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    @staticmethod
    def validate_username(nickname):
        user = User.query.filter_by(nickanem=nickname.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose different one.')

    @staticmethod
    def validate_email(email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That already exists in database. Please choose different one.')


class LoginFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    @staticmethod
    def validate_username(nickname):
        user = User.query.filter_by(nickname=nickname.data).first()
        if not user:
            raise ValidationError('There is no user with this nickname')
