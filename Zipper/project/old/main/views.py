from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from project.users.forms import LoginForm, RegisterForm

main = Blueprint('main',__name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('files.file'))
    login_form = LoginForm()
    signup_form = RegisterForm()
    error = False
    return render_template('index.html', login_form=login_form,
            signup_form=signup_form, error=error)

