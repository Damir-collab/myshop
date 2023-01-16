from flask import render_template, session, request, redirect, url_for, flash, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import app, db, photos, search, bcrypt, login_manager
from shop.customers.forms import CustomerRegisterForm, CustomerLoginForm
from shop.customers.model import Register, CustomerOrder
from yookassa import Configuration, Payment
import secrets
import os
import json
import pdfkit
import yookassa
import uuid

SHOP_ID = 973076
PAYMENT_TOKEN = 'test_I8vdgPmSuLG0aAv_nyl5Ki912ISzvIk1bS7BAxW7Mt0'
@app.route('/payment', methods=['POST'])
@login_required
def create_invoice():
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = PAYMENT_TOKEN
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')

    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://127.0.0.1:5000/"
        },
        "capture": True,
        "description": "Подробнее",
        "metadata": {
            "order_id": "Заказ"
        }
    })

    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).\
        order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Оплачено'
    db.session.commit()
    return redirect (payment.confirmation.confirmation_url)
# @app.route('/thanks')
# def thanks():
#     return render_template('customer/thank.html')


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, city=form.city.data,
                            contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Добро пожаловать, {form.name.data}, спасибо за регистрацию!', 'success')
        db.session.commit()

        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы вошли в профиль', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Вы неправильно ввели логин или пароль', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Ваш заказ принят', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Что-то пошло не так', 'danger')
            return redirect(url_for('get_cart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grand_total = 0
        subtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id,
                                               invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grand_total = ("%.2f" % (1.06 * float(subtotal)))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subtotal=subtotal, grand_total=grand_total,
                           customer=customer, orders=orders)

@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grand_total = 0
        subtotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id,
                                                   invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax = ("%.2f" % (.06 * float(subtotal)))
                grand_total = float("%.2f" % (1.06 * subtotal))

            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, grand_total=grand_total,
                                       customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'atteched; filename=' + invoice + '.pdf'
            return response
    return request(url_for('orders'))

def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart