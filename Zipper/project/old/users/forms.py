from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo,ValidationError, Length
from wtforms.fields.html5 import EmailField
from flask_login import current_user
from project.models import User
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()],
            render_kw={"id":"email","placeholder":"email aadress"})
    remember_me = BooleanField(render_kw={"id":"remember-me"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)],
            render_kw={"id":"password","placeholder":"password","class":"button"})
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()],
            render_kw={"id":"signUpName","placeholder":"username"})
    email = EmailField('email', validators=[DataRequired(), Email()],
            render_kw={"id":"signUpEmail","placeholder":"email address"})
    password = PasswordField('password', validators=[DataRequired(),Length(min=8)],
            render_kw={"id":"signUpPassword","placeholder":"password"})
    confirm_password = PasswordField('confirm_password',
            validators=[DataRequired(),EqualTo('password', message='Passwords not match')],
            render_kw={"id":"signUpConfirmPassword","placeholder":"confirm password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist')
        elif len(field.data) > 20:
            raise ValidationError('Maximum length exceeded')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address already exist')
        elif len(field.data) > 50:
            raise ValidationError('Maximum length exceeded')

class RequestForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()],
            render_kw={"placeholder":"Email address"})
    submit = SubmitField('Submit Request')

class ResetForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(),Length(min=8)],
            render_kw={"placeholder":"Enter Password"})
    confirm_password = PasswordField('confirm_password',
            validators=[DataRequired(),EqualTo('password', message='Passwords not match')],
            render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField('Reset Password')

class UpdateForm(FlaskForm):
    username = username = StringField('username', validators=[DataRequired()],
            render_kw={"id":"input-username", "class":"form-control form-control-alternative"})
    email = EmailField('email', validators=[DataRequired(), Email()],
            render_kw={"id":"input-email", "class":"form-control form-control-alternative"})
    profile_pic = FileField('Change Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])],
        render_kw={'id':'file'})
    current_password = PasswordField('password',
            render_kw={"id":"input-password", "class":"form-control form-control-alternative",
                "placeholder":"Current password"})
    password = PasswordField('password',
            render_kw={"id":"input-password", "class":"form-control form-control-alternative",
                "placeholder":"New password"})
    confirm_password = PasswordField('confirm_password',
            validators=[EqualTo('password', message='Password must match')],
            render_kw={"id":"input-password", "class":"form-control form-control-alternative",
                "placeholder":"confirm password"})
    submit = SubmitField('Update')

    def validate_current_password(self, field):
        if field.data:
            if not current_user.check_password(field.data):
                raise ValidationError('Password not match')
        elif self.password.data:
            raise ValidationError('enter your current password')

    def validate_password(self, field):
        if field.data:
            if len(field.data) < 8:
                raise ValidationError('Field Must be atleaset 8 charecter long')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() and \
                current_user.username != field.data:
            raise ValidationError('Username already exist')
        elif len(field.data) > 20:
            raise ValidationError('Maximum length exceeded')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() and \
                current_user.email != field.data:
            raise ValidationError('Email address already exist')
        elif len(field.data) > 50:
            raise ValidationError('Maximum length exceeded')
