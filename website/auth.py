from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User,Book, Cart, Genre,Order,OrderBook
from .forms import UpdateAccountForm
from datetime import datetime, date

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():

    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('Account does not exist',category='error')
    return render_template("login.html",user=current_user)


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account',user=current_user))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('account.html', title='Account', form=form, user=current_user)
     

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.',category='error')
    
    return redirect(url_for('auth.login'))



@auth.route('/signup',methods=['GET','POST'])
def signup():

    if request.method=='POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('confirmpassword')
        address = request.form.get('address')
        phone = request.form.get('phone')
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Account already exists',category='error')
        elif password != password1:
            flash('Passwords do not match',category='error')
        else:
            new_user = User(email=email, first_name= first_name,last_name = last_name, address = address, phone = phone, password=generate_password_hash(
            password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html",user=current_user)


@auth.route("/confirm")
def confirm():
    if current_user.is_authenticated:
        carts=Cart.query.filter_by(user_id=current_user.id).all()
        sum=0
        for cart in carts:
            sum=sum+cart.cartbook.price
        order=Order(user_id=current_user.id,amount=sum)
        db.session.add(order)
        db.session.commit()
        oid=order.id
        for cart in carts:
            orderbook=OrderBook(user_id=current_user.id,book_id=cart.cartbook.id,order_id=oid)
            cart.cartbook.quantity=cart.cartbook.quantity-1
            db.session.add(orderbook)
            db.session.commit()
            
        flash('Book has been Ordered Successfully', 'success')
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return redirect(url_for('auth.order'))
    return render_template('order.html', title="order",user=current_user) 

@auth.route("/order")
def order():
    orders=Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order.html', title="order",orders=orders,user=current_user) 


# receipt function
@auth.route("/receipt/<int:order_id>")
def receipt(order_id):
    order=Order.query.get_or_404(order_id)
    orderbook=OrderBook.query.filter_by(order_id=order_id)
    return render_template('receipt.html',title="testdemp", order = order, orderbook = orderbook, user = current_user)


@auth.route("/cancel")
@login_required
def cancel():
    flash('Transaction Cancelled', 'success')
    return redirect(url_for('views.cart'))
    