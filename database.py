from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    Invoice_number = db.Column(db.String(500), nullable=False)  # Ask about unique=True or not
    Invoice_date = db.Column(db.String(20), nullable=False)
    Product_name = db.Column(db.String(1500), unique=True, nullable=False)
    Batch_no = db.Column(db.String(100), nullable=False)
    Exp_date = db.Column(db.String(20), nullable=False)
    Original_price = db.Column(db.Numeric(12, 2), nullable=False)
    Discount_price = db.Column(db.Numeric(12, 2), nullable=False)
    Sheet_quantity = db.Column(db.Integer, nullable=False)
    Tablet_quantity = db.Column(db.Integer, nullable=False)
    Sheet_tablet_count_default = db.Column(db.Integer, nullable=False)
    Created_at = db.Column(db.DateTime, default=datetime.now())
    Updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # users = db.relationship('User', backref='product')

    def __repr__(self):
        return f"Product name:{self.Product_name}, Inv_num:{self.Invoice_number}"


class CheckOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Product_name = db.Column(db.String(1500), unique=True, nullable=False)
    Exp_date = db.Column(db.String(20), nullable=False)
    Original_price = db.Column(db.Numeric(12, 2), nullable=False)
    Discount_price = db.Column(db.Numeric(12, 2), nullable=False)
    Tablet_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product name:{self.Product_name}, Inv_num:{self.Discount_price}"


class UserProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(550), nullable=False)
    Phone_number = db.Column(db.String(10), nullable=False)
    Product_name = db.Column(db.String(1500), nullable=False)
    Exp_date = db.Column(db.String(20), nullable=False)
    Original_price = db.Column(db.Numeric(12, 2), nullable=False)
    Discount_price = db.Column(db.Numeric(12, 2), nullable=False)
    Tablet_quantity = db.Column(db.Integer, nullable=False)
    Recent_date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Product name:{self.Product_name}, Inv_num:{self.User_name}"
