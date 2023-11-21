import json
import logging

from flask import request, jsonify, Blueprint

from user import db
from books.models import Books

book = Blueprint("book", __name__, url_prefix="/books")


@book.route('/add_book', methods=["POST"])
def create():
    """
    bookstore curd operation
    :return: message successful or not
    """
    try:

        book_info = json.loads(request.data)
        book_name = book_info.get("book_name")
        author = book_info.get("author")
        price = book_info.get("price")

        newbook = Books(book_name=book_name, author=author, price=price)
        db.session.add(newbook)
        db.session.commit()
        return jsonify({
            "message": "new book is created",
            "data": newbook.__str__()
        })
    except Exception as e:
        logging.error(e)
        return jsonify({'message': str(e)})


@book.route("/get_book", methods=["GET"])
def get():
    """
    this method display all the books of specify user_id
    :param :
    :return: list of books info
    """
    try:

        books = Books.query.all()
        return jsonify({
            'Books': list(x.__str__() for x in books)
        })
    except Exception as e:
        logging.error(e)
        return jsonify({'message': "error"})


@book.route("/update_book", methods=["PUT"])
def put():
    """
    this method is to update book details if found
    :return:update info
    """
    try:

        data = request.get_json()
        book_name = data.get('book_name')
        book = Books.query.filter_by(book_name=book_name).first()
        if not book:
            return jsonify({
                "message": "Book name not found"
            })
        book.price = data.get("price")
        book.author = data.get("author")
        db.session.add(book)
        db.session.commit()
        return jsonify({
            "data": book.__str__()
        })
    except Exception as e:
        logging.error(e)
        return jsonify({
            "message": str(e)
        })


@book.route("/delete_book", methods=['DELETE'])
def book_delete():
    """
    this method is to delete book from books data
    :return:message is deleted
    """
    try:
        data = json.loads(request.data)
        book_name = data.get('book_name')
        book = Books.query.filter_by(book_name=book_name).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({
                'message': 'book deleted'
            })
        else:
            return jsonify({
                'message': 'book not found'
            })
    except Exception as e:
        logging.error(e)
        return jsonify({
            "message": str(e)
        })
