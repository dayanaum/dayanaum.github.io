import json
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .api import infoQuery
from .models import User, Book, Cart, Genre, Review

views = Blueprint('views',__name__)

@views.route('/')

def home():
    booksJOINgenre =  db.session.query(Book,Genre).select_from(Book).join(Genre).all()
    
    return render_template("index.html",user=current_user,combine=booksJOINgenre)

# book info rediect 
@views.route("book_info/<int:book_id>", methods=['GET','POST'])
def book_info(book_id):
    book = Book.query.get_or_404(book_id)
    bookinfoQuery = json.loads(infoQuery.info(book.title))
    reviewJOINuser =  db.session.query(Review,User).select_from(Review).join(User).filter(Review.bookid == book_id).order_by(Review.id.desc()).all()
    
    if request.method == 'POST':
        if current_user.is_authenticated:
            comment = request.form.get('comment')
            if len(comment.strip()) < 1:
                flash('Comment is too short' ,category='error')
            elif len(comment.strip()) > 1000:
                flash('Maximum comment size is 1000 characters' ,category='error')
            else:
                newComment = Review(data=comment, date = date.today(),user_id=current_user.id, bookid=book_id)
                db.session.add(newComment)
                db.session.commit()
                flash('Comment added.', category='success')
                return redirect(url_for('views.book_info', book_id=book_id))
        else:
            flash('Login to comment.', 'error')
            return redirect(url_for('auth.login'))  

    return render_template('book_info.html', title=book.title, book=book, user=current_user, info = bookinfoQuery["description"], commentList = reviewJOINuser)


#######################
# cart redirect
@views.route("/cart")
def cart():
    carts=Cart.query.filter_by(user_id=current_user.id).all()
    sum=0
    for cart in carts:
        sum=sum+cart.cartbook.price
    return render_template('cart.html', title="cart",carts=carts,total=sum,user=current_user)   

# Addbooks to cart
@views.route("/addcart/<int:book_id>")
def addcart(book_id):
    if current_user.is_authenticated:
        book = Book.query.get_or_404(book_id)
        cart=Cart(user_id=current_user.id,book_id=book_id)
        db.session.add(cart)
        db.session.commit()
        flash('Book added to cart', 'success')
        return redirect(url_for('views.cart'))
    else:
        flash('Login to add this book to your cart.', 'error')
        return redirect(url_for('auth.login'))

# Delete books from cart
@views.route("/cart/<int:cart_id>/delete_cart", methods=['POST'])
@login_required
def delete_cart(cart_id):
    if current_user.is_authenticated:
        cart = Cart.query.get_or_404(cart_id)
        db.session.delete(cart)
        db.session.commit()
        flash('Book deleted from cart.', 'error')
        return redirect(url_for('views.cart'))

# Checkout Cart
@views.route("/checkout")
def checkout():
    carts=Cart.query.filter_by(user_id=current_user.id).all()
    c=Cart.query.filter_by(user_id=current_user.id).first()
    sum=0
    for cart in carts:
        sum=sum+cart.cartbook.price
    return render_template('checkout.html', title="checkout",carts=carts,total=sum, user=current_user) 

@views.route("/cancel",methods=['POST'])
@login_required
def cancel():
    flash('Transaction Cancelled', 'success')
    return redirect(url_for('cart'))



