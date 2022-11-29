from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, PasswordField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm


class CustomerRegisterForm(Form):
    name = StringField('Имя: ')
    username = StringField('Никнейм: ', [validators.DataRequired()])
    email = StringField('Электронная почта: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(),
                                            validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Повторите пароль: ', [validators.DataRequired()])
    country = StringField('Страна: ', [validators.DataRequired()])
    city = StringField('Город: ', [validators.DataRequired()])
    state = StringField('Субъект: ', [validators.DataRequired()])
    contact = StringField('Контакты: ', [validators.DataRequired()])
    address = StringField('Адрес: ', [validators.DataRequired()])
    zipcode = StringField('Индекс: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])
    submit = SubmitField('Зарегистрироваться')

    # def validate_username(self, username):
    #     if Register.query.filter_by(username=username.data).first():
    #         raise ValidationError("This username is already in use!")
    #
    # def validate_email(self, email):
    #     if Register.query.filter_by(email=email.data).first():
    #         raise ValidationError("This email address is already in use!")