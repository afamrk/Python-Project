from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError
from wtforms.validators import EqualTo, DataRequired
from project.user.models import User

class RegisterForm(FlaskForm):

    email = EmailField('Enter your email address: ', validators=[DataRequired()])
    username = StringField('Enter your username: ', validators=[DataRequired()])
    password = PasswordField('Enter',
                             validators=[DataRequired(), EqualTo('password_confirm', message='passowrd must match')])
    password_confirm = PasswordField('Enter', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already Exist')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already Exist')

class LoginForm(FlaskForm):

    username = StringField('Enter your username: ', validators=[DataRequired()])
    password = PasswordField('Enter',
                             validators=[DataRequired()])
    submit = SubmitField('Login')

    def check_username(self, field):
        print(1)
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('username not Exist')
