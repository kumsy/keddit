from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import Users

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choosen another one.')

    def validate_email(self, email):

        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choosen another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CommunityForm(FlaskForm):
    title = StringField('Community Name', validators=[DataRequired()])
    submit = SubmitField('Post')
