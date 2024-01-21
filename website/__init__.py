from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

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
    
    from .models import Staff, Department, Room, Stock, Order, Supplier

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
        with app.app_context():
            db.create_all()
            print("Created Database")
            return
        print("Database Loaded")
        return