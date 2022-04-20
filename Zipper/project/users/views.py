from flask import render_template, redirect, Blueprint, request, flash, url_for, current_app
from werkzeug.security import generate_password_hash
from project.users.forms import LoginForm, RegisterForm, RequestForm, ResetForm, UpdateForm
from project.models import User
from project import db
from flask_login import login_user, logout_user, current_user, login_required
from project.users.utils import send_mail, pic_saver
from oauthlib.oauth2 import WebApplicationClient
import requests
import json,os
from project.config import Config
import secrets
from project.files.forms import LinkForm

# Configuration
GOOGLE_CLIENT_ID = Config.CLIENT_ID
GOOGLE_CLIENT_SECRET = Config.CLIENT_SECRET
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

users = Blueprint('users', __name__)

def pprint(message):
    print(f'\n#######\n{message}\n##########\n')
    
@users.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('files.file'))

    login_form = LoginForm()
    signup_form = RegisterForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Email address or Password is Incorrect','danger')
            return redirect(url_for('users.login'))
        if user:
            if not user.email_verified:
                send_mail(user, 'email_confirmation')
                flash('Please verify your email address,check your inbox for verification message','danger')
                return redirect(url_for('users.login'))

            login_user(user,remember=login_form.remember_me.data)
            next = request.args.get('next')
            if next is None or next[0] != '/':
                next = url_for('files.file')

            return redirect(next)
        
    error = 'login'
    return render_template('index.html', login_form=login_form,
            signup_form=signup_form, error=error)

@users.route("/google")
def google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://127.0.0.1/google/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@users.route("/google/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url="https://127.0.0.1/google/callback",
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    resp = requests.get(uri, headers=headers, data=body)
    if resp.ok:
        response = resp.json()
        user = User.query.filter_by(email=response['email']).first()
        if not user:
            r = requests.get(response['picture'])
            filename = f'{response["sub"]}.jpg'
            loc = os.path.join(current_app.root_path,'static/profile_pics',filename)
            with open(loc, 'wb') as f:
                f.write(r.content)
            user = User(
                username = response['name'],
                email = response['email'],
                password = secrets.token_hex(12),
                profile_pic = filename,
                email_verified = True
                )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('files.file'))
    else:
        flash('Something went Wrong','danger')
        return redirect(url_for('users.login'))


@users.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('files.file'))

    login_form = LoginForm()
    signup_form = RegisterForm()
    if signup_form.validate_on_submit():
        user = User(
                username = signup_form.username.data,
                email = signup_form.email.data,
                password = signup_form.password.data
                )
        db.session.add(user)
        db.session.commit()
        flash('Account Created Successfully','success')
        return redirect(url_for('users.login'))

    error = 'register'
    return render_template('index.html', login_form=login_form,
            signup_form=signup_form, error=error)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/varify_email/<token>', methods=['POST','GET'])
def email_verification(token):
    if current_user.is_authenticated:
        logout_user()
    user = User.check_token(token)
    if user is None:
        flash('This is an invalid or expired token','warning')
        return redirect(url_for('users.login'))
    user.email_verified = True
    db.session.commit()
    login_user(user)
    return redirect(url_for('files.file'))

@users.route('/password_request', methods=['GET','POST'])
def password_request():
    if current_user.is_authenticated:
        return redirect(url_for('files.file'))
    login_form = LoginForm()
    signup_form = RegisterForm()
    request_form = RequestForm()
    if request_form.validate_on_submit():
        user = User.query.filter_by(email=request_form.email.data).first()
        if user:
            send_mail(user, 'password_reset')
        flash('If an account with this email address exists, a password reset message will be sent shortly','info')
        return redirect(url_for('users.password_request'))
    error = False
    return render_template('password_request.html', login_form=login_form,
            signup_form=signup_form, request_form=request_form, error=error)

@users.route('/password_reset/<token>', methods=['GET','POST'])
def password_reset(token):
    if current_user.is_authenticated:
        logout_user()
    login_form = LoginForm()
    signup_form = RegisterForm()
    reset_form = ResetForm()
    user = User.check_token(token)
    if user is None:
        flash('This is an invalid or expired token','warning')
        return redirect(url_for('users.password_request'))
    if reset_form.validate_on_submit():
        password = generate_password_hash(reset_form.password.data)
        user.password_hash = password
        user.email_verified = True
        db.session.commit()
        flash('Your Password is successfully updated', 'success')
        return redirect(url_for('users.login'))

    error = False
    return render_template('password_reset.html', login_form=login_form,
            signup_form=signup_form, reset_form=reset_form, error=error)
    
@users.route('/account', methods=['POST','GET'])
@login_required
def account():
    update_form = UpdateForm()
    link_form = LinkForm()
    if update_form.validate_on_submit():
        if update_form.profile_pic.data:
            image_file = pic_saver(update_form.profile_pic.data,current_user.username)
            current_user.profile_pic = image_file
        current_user.username = update_form.username.data
        # if current_user.email != update_form.email.data:
        #     current_user.email_verified = False
        current_user.email = update_form.email.data
        if update_form.password.data:
            current_user.password_hash = generate_password_hash(update_form.password.data)
        db.session.commit()
        flash('Profile Updated Successfully','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    return render_template('account.html',update_form=update_form, link_form=link_form)
