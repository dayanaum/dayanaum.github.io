from flask_mail import Mail, Message
import os
from app import app

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('email')
app.config['MAIL_PASSWORD'] = os.environ.get('password')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def create_msg(email):
    subject = f'welcome, {email}'
    msg = Message(
        subject,
        sender=email,
        recipients=['dhugkar95@gmail.com']
    )
    msg.body = 'Welcome to book store app'
    return msg
