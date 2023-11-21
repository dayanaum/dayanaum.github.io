from user import db


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, book_name, author, price):
        self.book_name = book_name
        self.author = author
        self.price = price

    def __str__(self):
        return {"book_name": self.book_name, "author": self.author, "price": self.price}
