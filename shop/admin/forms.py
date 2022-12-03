from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import BooleanField, StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from shop.admin.models import User
class RegistrationForm(FlaskForm):
    name = StringField('Имя ', [validators.Length(min=4, max=25)])
    username = StringField('Никнейм', [validators.Length(min=4, max=25)])
    email = StringField('Электронный адрес', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField(' Новый пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароль должны совпадать')
    ])
    confirm = PasswordField('Повторите пароль')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(FlaskForm):
    password = password = PasswordField('   Password', [validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
