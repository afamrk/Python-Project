from flask_login import UserMixin
from flask import current_app
from project import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True, nullable=False)
    email = db.Column(db.String(50), unique=True, index=True, nullable=False)
    profile_pic = db.Column(db.String(30), nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(db.String(160), nullable=False)
    files = db.relationship('Folder', backref='owner', lazy='dynamic')

    def __init__(self, username, email, password, profile_pic='default.png', email_verified=False):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.profile_pic = profile_pic
        self.email_verified = email_verified


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, time=1800):
        s = Serializer(current_app.config['SECRET_KEY'], time)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User(id={self.id},username={self.username},email={self.email}'

class Folder(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    location = db.Column(db.String, nullable=False)
    file_location = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.String, nullable=False, default='Processing')
    splited = db.Column(db.Boolean, nullable=False, default=False)
    virus = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content_type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    subfiles = db.relationship('SubFiles', backref='main', lazy='dynamic')

    def __init__(self,name,location,size,user_id,file_location,splited=False, content_type='file'):
        self.name = name
        self.size = size
        self.location = location
        self.user_id = user_id
        self.splited = splited
        self.content_type = content_type
        self.file_location = file_location

    def get_token(self, time=86400):
        s = Serializer(current_app.config['SECRET_KEY'], time)
        return s.dumps({'folder_id':self.id}).decode('utf-8')
    
    @staticmethod
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            folder_id = s.loads(token)['folder_id']
        except:
            return None
        return Folder.query.get(folder_id)

    def __repr__(self):
        return f'Folder({self.name},{self.size},{self.content_type},{self.location},{self.file_location},{self.progress} ,{self.virus})'

class SubFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    location = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content_type = db.Column(db.String, nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'),nullable=False)

    def __init__(self,name,location,size,folder_id, content_type='file'):
        self.name = name
        self.size = size
        self.location = location
        self.folder_id = folder_id
        self.content_type = content_type

    def get_token(self, time=86400):
        s = Serializer(current_app.config['SECRET_KEY'], time)
        return s.dumps({'id':self.id}).decode('utf-8')
    
    @staticmethod
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            folder_id = s.loads(token)['id']
        except:
            return None
        return SubFiles.query.get(folder_id)

    def __repr__(self):
        return f'SubFiles({self.name},{self.size},{self.location},{self.folder_id})'

