from flask import redirect, render_template, url_for, flash, request
from shop import db, app, photos
from .models import Brand, Category, Addproduct
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
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        image_1= photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2= photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3= photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, color=color,
                            description=description, category_id=category, brand_id=brand,
                            image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', form=form, title="Add product page", brands=brands, categories=categories)