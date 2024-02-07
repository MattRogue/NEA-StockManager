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
    orders_requested = db.relationship(
        'Orders',
        foreign_keys='Orders.staff_requested_id',
        back_populates='staff_requested'
    )
    orders_accepted = db.relationship(
        'Orders',
        foreign_keys='Orders.staff_accepted_id',
        back_populates='staff_accepted',
        primaryjoin=and_(
            Staff.type==StaffType.HEAD,
            Staff.id==db.foreign("Orders.staff_accepted_id"))
    )
    orders_ordered = db.relationship(
        'Orders',
        foreign_keys='Orders.staff_ordered_id',
        back_populates='staff_ordered',
        primaryjoin=and_(
            department_id.name=="ADMIN",
            Staff.id==db.foreign("Orders.staff_ordered_id"))
    )

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
    #relationships
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    staff_requested_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    staff_accepted_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staff_ordered_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staff_requested = db.relationship(
        "Staff",
        foreign_keys=[staff_requested_id],
        back_populates="orders_requested"
        )
    staff_accepted = db.relationship(
        "Staff",
        foreign_keys=[staff_accepted_id],
        back_populates="orders_accepted"
        )
    staff_ordered = db.relationship(
        "Staff",
        foreign_keys=[staff_ordered_id],
        back_populates="orders_ordered"
        )
        