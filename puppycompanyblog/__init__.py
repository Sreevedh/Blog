# puppycompanyblog/__init__.py
# Where all things are merged 
# Hold most of our flask application logic and "blueprint logic."
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager



app = Flask(__name__)



########################################
############ DATABASE SETUP ############
########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'


db = SQLAlchemy(app)

Migrate(app,db)


########################################
########### Flask-Login Configurations ########
########################################
login_manager = LoginManager()
login_manager.init_app(app)

# here "users" is the blueprint template.
login_manager.login_view = 'users.login'


################################################
############ Connecting blueprints #############
################################################
#Blueprint of core
from puppycompanyblog.core.views import core
app.register_blueprint(core)

# Blueprint of error pages
from puppycompanyblog.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

from puppycompanyblog.users.views import users
app.register_blueprint(users)

from puppycompanyblog.blogpost.views import blogpost
app.register_blueprint(blogpost)


