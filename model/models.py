import datetime

from config import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_type_id = db.Column(db.ForeignKey("product_type.id"))
    serial_number = db.Column(db.String(100))
    name = db.Column(db.String(100))
    year = db.Column(db.String(100))

    productType = db.relationship("ProductType", uselist=False, backref=db.backref("Product", lazy="dynamic"))

    def __init__(self, serial_number, product_type_id):
        self.serial_number = serial_number
        self.product_type_id = product_type_id


class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    phone = db.Column(db.String(50))

    def __init__(self, name, surname, phone):
        self.name = name
        self.surname = surname
        self.phone = phone


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    user_role_id = db.Column(db.ForeignKey("user_role.id"), primary_key=True, nullable=False)

    userRole = db.relationship("UserRole", uselist=False, backref=db.backref("User", lazy="dynamic"))

    def __init__(self, name, surname, username, password, user_role_id, ):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.user_role_id = user_role_id


class Warranty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount_month = db.Column(db.Integer)

    def __init__(self, amount_month):
        self.amount_month = amount_month


class StateGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


class ProductState(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_group_id = db.Column(db.ForeignKey("state_group.id"), primary_key=True, nullable=False)
    name = db.Column(db.String(100))

    stateGroup = db.relationship("StateGroup", uselist=False, backref=db.backref("ProductState", lazy="dynamic"))

    def __init__(self, name, state_group_id, stateGroup):
        self.name = name
        self.state_group_id = state_group_id
        self.stateGroup = stateGroup


class CustomerProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.ForeignKey("product.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True, nullable=False)
    product_state_id = db.Column(db.ForeignKey("product_state.id"), primary_key=True, nullable=False)
    warranty_id = db.Column(db.ForeignKey("warranty.id"), primary_key=True, nullable=False)
    product_type_id = db.Column(db.ForeignKey("product_type.id"), primary_key=True, nullable=False)

    product = db.relationship("Product", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))
    customer = db.relationship("Customer", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))
    user = db.relationship("User", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))
    productState = db.relationship("ProductState", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))
    warranty = db.relationship("Warranty", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))
    productType = db.relationship("ProductType", uselist=False, backref=db.backref("CustomerProduct", lazy="dynamic"))

    price = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    return_date = db.Column(db.DateTime, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, product_id, customer_id, user_id, product_state_id, warranty_id, price, notes, return_date,
                 creation_date):
        self.product_id = product_id
        self.customer_id = customer_id
        self.user_id = user_id
        self.product_state_id = product_state_id
        self.price = price
        self.notes = notes
        self.return_date = return_date
        self.creation_date = creation_date
        self.warranty_id = warranty_id

