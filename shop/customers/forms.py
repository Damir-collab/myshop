from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, PasswordField, TextAreaField, validators,ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from shop.customers.model import Register
from flask_wtf import FlaskForm, From
from shop.admin.models import User


class CustomerRegisterForm(FlaskForm):
    name = StringField('Имя: ')
    username = StringField('Никнейм: ', [validators.DataRequired()])
    email = StringField('Электронная почта: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Повторите пароль: ', [validators.DataRequired()])
    country = StringField('Страна: ', [validators.DataRequired()])
    city = StringField('Город: ', [validators.DataRequired()])
    contact = StringField('Контакты: ', [validators.DataRequired()])
    address = StringField('Адрес: ', [validators.DataRequired()])
    zipcode = StringField('Индекс: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])
    submit = SubmitField('Зарегистрироваться')
    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Yикнеймом уже существует!")

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Электронная почта уже используется!")

class CustomerLoginForm(FlaskForm):
    email = StringField('Электронная почта: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired()])