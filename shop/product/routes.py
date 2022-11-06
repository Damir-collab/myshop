from flask import redirect, render_template, url_for, flash, request
from shop import db, app, photos
from .models import Brand, Category
from .forms import Addproducts
import secrets

@app.route('/')
def home():
    return "  "
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()

        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The category {getcategory} was added to your database', 'success')
        db.session.commit()

        return redirect(url_for('addcategory'))

    return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)

    if request.method == "POST":
        photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

    return render_template('products/addproduct.html', form=form, title="Add product page", brands=brands, categories=categories)