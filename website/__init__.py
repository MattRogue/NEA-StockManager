from os import getenv

from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
load_dotenv()
DB_NAME = getenv("DB_NAME")

def create_database(app):
    from os import path
    if not path.exists("instance/"+DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database")
        print("Database Loaded")
        return

def create_app():
    from datetime import timedelta
    
    from flask import Flask
    from flask_login import LoginManager
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "test"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Staff, Department, Room, Stock, Orders, Supplier, \
        StaffType, generate_password_hash, check_staff
        
    create_database(app)
    
    with app.app_context():
        #Verify default account
        DEFAULT_EMAIL = getenv("DEFAULT_EMAIL")
        DEFAULT_PASSWORD = getenv("DEFAULT_PASSWORD")
        
        if not check_staff(DEFAULT_EMAIL, DEFAULT_PASSWORD):
            ##Initialise department and account        
            admin_department = Department(name="ADMIN")
            db.session.add(admin_department)
            db.session.commit()
                    
            default_account = Staff(
                email=DEFAULT_EMAIL,
                password=generate_password_hash(DEFAULT_PASSWORD),
                type=StaffType.HEAD,
                department=admin_department
            )
            db.session.add(default_account)
            db.session.commit()
                    
    manager = LoginManager()
    manager.login_view = "auth.login"
    manager.init_app(app)
    
    @manager.user_loader
    def load_user(id):
        return Staff.query.get(int(id))

    return app

