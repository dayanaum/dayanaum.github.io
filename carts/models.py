from sqlalchemy.orm import relationship

from user import db


class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    total_quantity = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # created_at=db.Column(db.Date)
    # is_deleted=db.Column(db.Integer)
    user = relationship("Users")
    cart_item = relationship("CartItem", cascade="all, delete")


class CartItem(db.Model):
    cart_item_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.cart_id"))
    quantity = db.Column(db.Integer)
    book = relationship("Books")
    user = relationship("Users")
    cart = relationship("Cart", overlaps="cart_item")
