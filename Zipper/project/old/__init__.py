from flask import Flask
from project.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
Migrate(app, db)


login_manager.login_view = 'main.home'
login_manager.login_message_category = 'info'
mail = Mail(app)

#register blueprint
from project.main.views import main
app.register_blueprint(main)

from project.users.views import users
app.register_blueprint(users)

from project.files.views import files
app.register_blueprint(files)

from project.errors.views import errors
app.register_blueprint(errors)
