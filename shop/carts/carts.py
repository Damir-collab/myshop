import os
import secrets

from flask import redirect, session, render_template, url_for, flash, request, current_app

from shop import db, app, photos
from shop.product.forms import Addproducts
from shop.product.models import Brand, Category, Addproduct
from shop.product.routes import brands , categories


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price':float(product.price), 'discount': product.discount,
                                      'color': colors, 'quantity': quantity, 'image': product.image_1,
                                      'colors': product.color}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print(" Продукт находится в корзине ")
        #             # for key, item in session['Shoppingcart'].items():
        #             #     if int(key) == int(product_id):
        #             #         session.modified = True
        #             #         item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def get_cart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))

    subtotal = 0
    grand_total = 0

    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grand_total = float("%.2f" % (1.06 * subtotal))

    return render_template('products/carts.html', tax=tax, grand_total=grand_total, brands=brands(),
                           categories=categories())

@app.route('/updatecart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            pass
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Изменения сохранены', 'success')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/deleteitem/<int:id>')
def delete_item(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('get_cart'))