from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First name',validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Phone',validators=[DataRequired()])
    address= StringField ('Address',validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
                