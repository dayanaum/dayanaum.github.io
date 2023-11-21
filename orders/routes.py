import json
import logging

from flask import Blueprint, request

from books.models import Books
from orders.utils import get_format
from user import db

from orders.models import Orders, OrderItems

logging.basicConfig(filename='order_route.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
order = Blueprint("order", __name__, url_prefix="/orders")


@order.route("/add_order", methods=["POST"])
def add_order():
    """
    this method is for adding order,order_item in database
    :return: added successfully or not
    """
    try:
        order_data = json.loads(request.data)
        user_id = order_data.get("user_id")
        book_list = order_data.get("book_list")
        status = order_data.get("status")
        total_quantity = sum(book.get("quantity") for book in book_list)
        total_price = 0
        for book in book_list:
            books = db.session.query(Books).filter_by(book_id=book.get("book_id")).one()
            total_price += books.price * book.get("quantity")
        new_order = Orders(user_id=user_id, total_price=total_price, total_quantity=total_quantity, status=status)
        db.session.add(new_order)
        db.session.commit()
        for book in book_list:
            new_order_item = OrderItems(
                book_id=book.get("book_id"), user_id=user_id,
                quantity=book.get("quantity"), order_id=new_order.order_id)
            db.session.add(new_order_item)
            db.session.commit()
        return {
                   "order_id": new_order.order_id,
                   "message": "order add successfully"
               }, 201
    except Exception as e:
        print(e)
        logging.error(e)
        return {
            "message": "error"
        }


@order.route("/delete_order", methods=["DELETE"])
def delete_order():
    """
    this method is for delete order
    :return: delete successfully or not
    """
    try:
        request_data = json.loads(request.data)
        order_id = request_data.get("order_id")
        # order_item = OrderItems.query.filter_by(order_id=order_id).delete()
        order_item = OrderItems.query.filter_by(order_id=order_id).all()
        for item in order_item:
            db.session.delete(item)
            db.session.commit()
        order_data = Orders.query.get(order_id)
        db.session.delete(order_data)
        db.session.commit()
        return {
                   "message": "delete successfully"
               }, 204
    except Exception as e:
        logging.error(e)
        return {
            "error_message": str(e)
        }


@order.route("/get_order_by_userid", methods=["GET"])
def get_by_userid():
    """
    get all the order by user_id
    :return: order_list
    """
    try:
        request_data = json.loads(request.data)
        user_id = request_data.get("user_id")
        data = db.session.query(OrderItems, Orders, Books) \
            .outerjoin(Orders, OrderItems.order_id == Orders.order_id) \
            .outerjoin(Books, OrderItems.book_id == Books.book_id) \
            .filter(OrderItems.user_id == user_id).all()
        print(data)
        order_list = get_format(data)
        return {
            "message": order_list
        }
    except Exception as e:
        logging.error(e)
        return {
            "error_message": str(e)
        }
