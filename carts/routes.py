import json
import logging

from flask import Blueprint, request

from books.models import Books
from orders.models import Orders, OrderItems
from user import db
from .models import Cart, CartItem

carts = Blueprint("carts", __name__, url_prefix="/carts")


@carts.route("/add_cart", methods=["POST"])
def add_cart():
    """
    get request userid and booklist and
    add to cart and cart item in database
    :return: cart_id, message
    """
    try:
        request_data = json.loads(request.data)
        book_list = request_data.get("book_list")
        user_id = request_data.get("user_id")
        total_price = 0
        total_quantity = sum([x.get("quantity") for x in book_list])
        print(total_quantity)
        for book in book_list:
            print("a")
            books = db.session.query(Books).filter_by(book_id=book.get("book_id")).one()
            print(books.price)
            total_price += books.price * book.get("quantity")
        cur_cart = db.session.query(Cart).filter_by(user_id=user_id, status=0).first()
        # 0-active 1-inactive
        if not cur_cart:
            print("new")
            cur_cart = Cart(total_quantity=total_quantity, total_price=total_price, status=0, user_id=user_id)
            db.session.add(cur_cart)
            db.session.commit()
        else:
            print("old")
            cur_cart.total_price = cur_cart.total_price + total_price
        for book in book_list:
            cart_item = CartItem(
                user_id=user_id, cart_id=cur_cart.cart_id,
                book_id=book.get("book_id"), quantity=book.get('quantity'))
            db.session.add(cart_item)
            db.session.commit()
        return {
            "cart_id": cur_cart.cart_id,
            "message": "cart added successfully"
        }

    except Exception as e:
        return {
            "error_message": str(e)
        }


@carts.route("/getcart", methods=["GET"])
def get_cart():
    """
    get all the cart item by cart_id
    :return: cart_list
    """
    request_data = json.loads(request.data)
    user_id = request_data.get("user_id")
    cart_data = db.session.query(CartItem, Cart, Books) \
        .outerjoin(Cart, CartItem.cart_id == Cart.cart_id) \
        .outerjoin(Books, CartItem.book_id == Books.book_id) \
        .filter(CartItem.user_id == user_id, Cart.status == 0) \
        .all()
    if len(cart_data) == 0:
        return {
            "message": "no cart found"
        }
    cart_list = []
    for cart in cart_data:
        cart_list.append({
            "book_name": cart[2].book_name,
            "price": cart[2].price,
        })
    return {
        "user_id": user_id,
        "cart_data": cart_list
    }


@carts.route("/delete_cart", methods=["DELETE"])
def delete_cart():
    """
    delete cart with cart items
    :return: message
    """
    try:
        request_data = json.loads(request.data)
        cart_id = request_data.get("cart_id")
        CartItem.query.filter_by(cart_id=cart_id).delete()
        Cart.query.filter_by(cart_id=cart_id).delete()
        db.session.commit()
        return {
            "message": "delete successfully"
        }
    except Exception as e:
        logging.error(e)
        return {
            "error_message": str(e)
        }


@carts.route('/cart_to_order', methods=["POST"])
def add_cart_to_order():
    """
    this method is for adding cart data in order data by user_id and cart_id
    :return: added successfully or error
    """
    try:
        request_data = json.loads(request.data)
        user_id = request_data.get('user_id')
        cart_id = request_data.get('cart_id')
        print(request_data)

        cart_data = db.session.query(CartItem, Cart) \
            .outerjoin(Cart, CartItem.cart_id == Cart.cart_id) \
            .filter_by(user_id=user_id, cart_id=cart_id, status=0) \
            .all()
        if not cart_data:
            return {
                "message": "cart not found to add"
            }
        new_order = Orders(
            user_id=request_data.get('user_id'), total_price=cart_data[1].Cart.total_price,
            total_quantity=cart_data[1].Cart.total_quantity, status=1)
        db.session.add(new_order)
        db.session.commit()
        for cart_item in cart_data:
            new_order_item = OrderItems(
                book_id=cart_item[0].book_id, user_id=cart_item[0].user_id,
                quantity=cart_item[0].quantity, order_id=new_order.order_id)
            db.session.add(new_order_item)
            db.session.commit()
        close_status = db.session.query(Cart).filter_by(user_id=user_id, status=0).first()
        close_status.status = 1
        db.session.commit()

        return {
            "message": "cart add to order successfully"
        }

    except Exception as e:
        logging.error(e)
        return {
            "error_message": str(e)
        }
