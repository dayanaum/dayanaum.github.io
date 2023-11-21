from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Review(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     data = db.Column(db.String(1000))
     date = db.Column(db.DateTime(timezone = True), default=func.now)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     
     bookid = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

     def __repr__(self):
        return f"User('{self.user_id}','{self.bookid}', '{self.data}')"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))
    order=db.relationship('Order', backref='buyer', lazy=True)
    orderbook=db.relationship('OrderBook', backref='orderby', lazy=True)
    review = db.relationship('Review')

    def __repr__(self):
        return f"User('{self.id}', '{self.first_name}', '{self.last_name}')"
    

class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication = db.Column(db.String(100), nullable=False)
    ISBN = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    cart=db.relationship('Cart', backref='cartbook', lazy=True)
    orderbook=db.relationship('OrderBook', backref='orderbook', lazy=True)
    review = db.relationship('Review', backref='review', lazy=True) 
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.publication}', '{self.ISBN}', '{self.price}', '{self.image_file}', '{self.genre_id}' )"

class Genre(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    genre_name = db.Column(db.String(50), nullable=False)
    book = db.relationship('Book', backref='genre', lazy=True)
    def __repr__(self):
        return f"Genre('{self.id}','{self.genre_name}')"



class Cart(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)



    def __repr__(self):
        return f"Cart('{self.id}', '{self.user_id}', '{self.book_id}')" 


class Order(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime(timezone = True), nullable=False, default=datetime.utcnow)
    orderbook=db.relationship('OrderBook', backref='orderdetail', lazy=True)
    

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}','{self.amount}','{self.order_date}')" 


class OrderBook(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    order_id= db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    

    def __repr__(self):
        return f"OrderBook('{self.id}', '{self.user_id}','{self.book_id}','{self.order_id}')"       

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.email}')" 