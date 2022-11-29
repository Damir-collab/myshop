import os
import secrets
from flask import redirect, session, render_template, url_for, flash, request, current_app
from shop import db, app, photos, search, bcrypt
from shop.customers.forms import CustomerRegisterForm
from shop.customers.model import Register

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, state=form.state.data,
                            city=form.city.data, contact=form.contact.data, address=form.address.data,
                            zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Добро пожаловать, {form.name.data}, спасибо за регистрацию!', 'success')
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)
