from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from project.config import Config
from flask_socketio import SocketIO

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'user.login'


from project.user.views import user
app.register_blueprint(user, url_prefix='/user')

from project.chat.views import chat
app.register_blueprint(chat, url_prefix='/chat')