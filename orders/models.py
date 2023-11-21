from sqlalchemy.orm import relationship

from user import db


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total_price = db.Column(db.Float, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user = relationship("Users")
    # order_item = relationship("Order_items", cascade="all, delete")


class OrderItems(db.Model):
    order_items_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    order = relationship("Orders")
    book = relationship("Books")

    def __init__(self, book_id, user_id, quantity, order_id):
        self.book_id = book_id,
        self.user_id = user_id,
        self.quantity = quantity,
        self.order_id = order_id
