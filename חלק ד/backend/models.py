from app import db
from sqlalchemy import Enum

class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15))
    representative_name = db.Column(db.String(100))
    password = db.Column(db.String(255))
    role = db.Column(db.String(50), default="supplier") 

    goods = db.relationship('Goods', backref='suppliers', lazy=True)
    orders = db.relationship('Orders', backref='suppliers', lazy=True)

class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price_per_item = db.Column(db.Float)
    min_quantity = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    status = db.Column(Enum('new','Pending', 'Completed', name='status_enum'), default='Pending')
    products = db.Column(db.JSON)  # Assuming products is a JSON field
    company_name = db.Column(db.String(255))
    representative_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))