from os import path, getenv
from datetime import timedelta

from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
load_dotenv()
DB_NAME = getenv("DB_NAME")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "test"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Staff, Department, Room, \
        Stock, Orders, Supplier
        
    create_database(app)

    manager = LoginManager()
    manager.login_view = "auth.login"
    manager.init_app(app)
    
    @manager.user_loader
    def load_user(id):
        return Staff.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("instance/"+DB_NAME):
        from .utils import create_staff
        with app.app_context():
            db.create_all()
            print("Created Database")
            #Verify default account
            DEFAULT_EMAIL = getenv("DEFAULT_EMAIL")
            DEFAULT_PASSWORD = getenv("DEFAULT_PASSWORD")
            default_account = create_staff(
                email=DEFAULT_EMAIL,
                password=DEFAULT_PASSWORD,
                firstname="NULL",
                surname="NULL",
                type="HEAD"
            )
            if not default_account:
                raise Exception("Error: Failed to load default account")
            return
        print("Database Loaded")
        return