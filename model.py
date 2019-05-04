from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import enum
from sqlalchemy import Enum

from flask_login import LoginManager, UserMixin


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1:3306/shoptobd'


db = SQLAlchemy(app)
login_manager = LoginManager(app=app)




class Customer(db.Model,UserMixin):
    __tablename__ = 'customer'
    uid = db.Column(db.BigInteger,primary_key=True,autoincrement=True)#uid = unique id
    email = db.Column(db.String(50),nullable=False,unique=True,index=True)
    password=db.Column(db.String(100),nullable=False)
    address = db.Column(db.Text,nullable=False)
    phone = db.Column(db.String(14),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    fb_link = db.Column(db.Text,nullable=True)
    rel_orders = db.relationship('Order',back_populates='rel_customer',lazy="joined")

    def __init__(self,email,password,address,phone,name,**kwargs):
        super(Customer, self).__init__(**kwargs)
        self.email = email
        self.password = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt(rounds=16))
        self.phone = phone
        self.address = address
        self.name = name

class InvoiceStatusEnum(enum.Enum):
    INITIAL_INVOICE = 'Initial Invoice'
    FINAL_INVOICE = 'Final Invoice'

class ProductStatusEnum(enum.Enum):
    REVIEW_PENDING = 'Review Pending'
    REVIEW_DONE = 'Review Done'
    ORDER_PLACED = 'Order Placed'
    DELIVERY_COMPLETE ='Delivery Complete'
    ITEM_CANCELLED = 'Item Cancelled'



class Product(db.Model):
    __tablename__ = 'product'
    uid = db.Column(db.BigInteger,primary_key=True,autoincrement=True)#uid = unique id
    order_id = db.Column(db.BigInteger,db.ForeignKey('order.uid'))
    link = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text,nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    name =  db.Column(db.Text,nullable=True)
    price = db.Column(db.Float,nullable=True)
    shipping_charge = db.Column(db.Float,nullable=True)
    tax = db.Column(db.Float,nullable=True)
    weight_charge = db.Column(db.Float,nullable=True)
    status = db.Column(Enum(ProductStatusEnum),nullable=False,default=ProductStatusEnum.REVIEW_PENDING)
    rel_order = db.relationship('Order',back_populates='rel_products',lazy='joined')

    def __init__(self,order_id,link,description,quantity,**kwargs):
        super(Product,self).__init__(**kwargs)
        self.order_id = order_id
        self.link = link
        self.description = description
        self.quantity = quantity


class Order(db.Model):
    __tablename__ = 'order'
    uid = db.Column(db.BigInteger,primary_key=True,autoincrement=True)#uid = unique id
    customer_id = db.Column(db.BigInteger,db.ForeignKey('customer.uid'))
    order_date = db.Column(db.DateTime,default=datetime.now)
    invoice_status = db.Column(Enum(InvoiceStatusEnum), nullable=True,default=InvoiceStatusEnum.INITIAL_INVOICE)
    invoice_issue_date = db.Column(db.DateTime,nullable=True)
    rel_products = db.relationship('Product',back_populates="rel_order",lazy="joined")
    rel_customer = db.relationship('Customer', back_populates='rel_orders',lazy='joined')

    def __init__(self,customer_id):
        self.customer_id = customer_id
    







