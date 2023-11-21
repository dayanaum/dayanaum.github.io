from flask import Flask,render_template, redirect, url_for
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from logging import debug
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

SQLALCHEMY_TRACK_MODIFICATIONS = False

#database connection
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'password'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .models import User, Review, Book,Order

    #admin testing
    admin = Admin(app)
    admin.add_view(ModelView(Book, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(Review, db.session))
    admin.add_view(ModelView(User, db.session))
  
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('Github/Bookstore/website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')








