from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


#define all tables here
class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    type = db.Column(db.String(15), nullable=False) #Literal(Teacher, Head, Admin)
    department = db.Column(db.Integer, db.ForeignKey('department.id')) #foreign
    room = db.Column(db.Integer, db.ForeignKey('room.id')) #foreign
    orders = db.relationship('Order') #M:1 relationship - Many side

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    budget = db.Column(db.Integer) #Mult 100 to hold pennies as int
    staff = db.relationship('Staff')
    stock = db.relationship('Stock')
    orders = db.relationship('Order')

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    staff_members = db.relationship('Staff')
    stock = db.relationship('Stock')
    orders = db.relationship('Order')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    quantity = db.Column(db.Integer)
    damaged = db.Column(db.Integer)
    department = db.Column(db.Integer, db.ForeignKey('department.id')) #foreign
    room = db.Column(db.Integer, db.ForeignKey('room.id')) #foreign
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15))
    priority = db.Column(db.Integer)
    status = db.Column(db.String(15))
    quantity = db.Column(db.Integer)
    made = db.Column(db
    arrival
    stock = db.Column(db.Integer, db.ForeignKey('supplier.id')) #foreign
    room = db.Column(db.Integer, db.ForeignKey('room.id')) #foreign
    department = db.Column(db.Integer, db.ForeignKey('department.id')) #foreign
    staff = db.Column(db.Integer, db.ForeignKey('staff.id')) #foreign
    supplier = db.Column(db.Integer, db.ForeignKey('staff.id')) #foreign

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    link = db.Column(db.String(150))
    stock = db.relationship('Stock')
    orders = db.relationship('Order')
    
####################################################
def create_staff(email: str,
        password: str,
        firstname: str,
        surname: str,
        type: str) :

    if Staff.query.filter_by(email = email).first():
        return False
    
    user = Staff(email = email,
        password = generate_password_hash(password),
        firstname = firstname,
        surname = surname,
        type = type)
    db.session.add(user)
    db.session.commit()
    return user

def check_staff(email: str, password: str) -> bool:
    user = Staff.query.filter_by(email = email).first()
    if user and check_password_hash(user.password, password):
        return user
    return False