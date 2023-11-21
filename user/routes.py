import json
import logging

from flask import request, jsonify, Blueprint

from app import mail
from user import db
from user.email.email import create_msg
from user.models import Users

logging.basicConfig(filename='routes.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

user = Blueprint("user", __name__, url_prefix='/user')


@user.route("/signup", methods=["POST"])
def signup():
    """
    this method is for creating user info
    :return: message is created or not
    """
    # print("Reach signup")
    try:
        if request.method == "POST":
            userdata = json.loads(request.data)
            username = userdata.get('username')
            email = userdata.get('email')
            password = userdata.get("password")
            if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
                return jsonify({
                    "message": "duplicate found in username or userid or email "
                })
            user = Users(username=username, email=email, password=password)
            mail.send(create_msg(email))
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "user is created "})
    except Exception as e:
        logging.error(e)
        return jsonify({"message": str(e)})


@user.route("/signin", methods=["POST"])
def signin():
    """
    This method is used for signin purpose
    :return: message if successful or unsuccessful
    """
    try:
        if request.method == "POST":
            userdata = json.loads(request.data)
            username = userdata.get("username")
            password = userdata.get("password")
            # print(username, password)
            is_signin = Users.query.filter_by(username=username, password=password).first()
            # print(is_signin)
            if not is_signin:
                return jsonify({"message": "user signin unsuccessful"})
            return jsonify({"message": "user signin successfully"})

    except Exception as e:
        logging.error(e)
        return jsonify({"message": str(e)})
