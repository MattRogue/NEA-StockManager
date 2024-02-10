from . import db
from enum import Enum, auto
from flask_login import UserMixin
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


#define Enum classes
class StaffType(Enum):
    TEMP = auto()
    TEACHER = auto()
    HEAD = auto()
    
class OrderType(Enum):
    REQUEST = auto()
    ORDER = auto()

class OrderStatus(Enum):
    REQUESTED = auto()
    ACCEPTED = auto()
    ORDERED = auto()
    COMPLETED = auto()

#Association Tables for M:M relationships
requested = db.Table("requested",
    db.Column("staff_id", db.Integer, db.ForeignKey("staff.id")),
    db.Column("orders_id", db.Integer, db.ForeignKey("orders.id"))
)
accepted = db.Table("accepted",
    db.Column("staff_id", db.Integer, db.ForeignKey("staff.id")),
    db.Column("orders_id", db.Integer, db.ForeignKey("orders.id"))
)

ordered = db.Table("ordered",
    db.Column("staff_id", db.Integer, db.ForeignKey("staff.id")),
    db.Column("orders_id", db.Integer, db.ForeignKey("orders.id"))
)
#define database tables
class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    type = db.Column(db.Enum(StaffType), nullable=False)
    #relationships
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Integer, default=0) #in pennies
    #relationships
    staff = db.relationship("Staff", backref="department")
    stock = db.relationship("Stock", backref="department")
    orders = db.relationship("Orders", backref="department")

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(15), nullable=False)
    #relationships
    staff = db.relationship("Staff", backref="room")
    stock = db.relationship("Stock", backref="room")
    orders = db.relationship("Orders", backref="room")
    
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    link = db.Column(db.String(150))
    #relationships
    stock =  db.relationship("Stock", backref="supplier")

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    damaged = db.Column(db.Integer, default=0)
    #relationships
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Enum(OrderType), nullable=False)
    priority = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    arriving = db.Column(db.DateTime)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    #relationships
    requested_by = db.relationship(
        "Staff",
        secondary="requested",
        backref="requested_orders"
    )
    orders_accepted = db.relationship(
        "Staff",
        secondary="accepted",
        backref="accepted_orders"
    )
    orders_ordered = db.relationship(
        "Staff",
        secondary="ordered",
        backref="ordered_orders"
    )

##################

##Require department, redundant fname and sname
def create_staff(email: str, password: str, firstname: str, surname: str, type: str):
    if Staff.query.filter_by(email=email).first():
        return False

    try:
        type = StaffType[type.upper()]
    except KeyError:
        raise Exception("KeyError: StaffType accepts only TEMP, TEACHER, HEAD")
        return False

    user = Staff(
        email=email,
        password=generate_password_hash(password),
        firstname=firstname,
        surname=surname,
        type=type
    )
    db.session.add(user)
    db.session.commit()
    return user

def check_staff(email: str, password: str):
    user = Staff.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return False
