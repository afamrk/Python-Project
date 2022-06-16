from project.user.models import User
from project.user.forms import RegisterForm, LoginForm
from flask import render_template, redirect, session, Blueprint, url_for, request
from project import db,app
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps


user = Blueprint('user', __name__, template_folder='templates')

def not_login(func):
    """
    if a user is current logged in and try to access to access pages
    like login/register , then redirect the user to welcome page
    :param func:
    :return:
    """
    @wraps(func)
    def inner(*args,**kwargs):
        if current_user.is_authenticated:
            print('running')
            return redirect(url_for('user.welcome'))
        else:
            return func(*args, **kwargs)
    return inner

@user.route('/register', methods=['GET', 'POST'])
@not_login
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(form.email.data, form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)

@user.route('/login', methods=['GET', 'POST'])
@not_login
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_user(form.password.data):
            login_user(user)
            next_ =  request.args.get('next')
            if not next_:
                next_ = url_for('user.welcome')

            return redirect(next_)
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user.route('/welcome')
@login_required
def welcome():
    room_id = request.args.get('room')
    if room_id:
        session['room_id'] = room_id
        return redirect(url_for('chat.chat_page'))
    return render_template('user/welcome_user.html')



