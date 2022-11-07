from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets
import os

@app.route('/')
def home():
    return "  "
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()

        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    if request.method == "POST":
        flash(f'The brand {updatebrand.name} was changed to {brand}', 'success')
        updatebrand.name = brand
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Update brand', updatebrand=updatebrand)

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
        if request.method == "POST":
            getcategory = request.form.get('category')
            category = Category(name=getcategory)
            db.session.add(category)
            flash(f'The category {getcategory} was added to your database', 'success')
            db.session.commit()

            return redirect(url_for('addcategory'))

    return render_template('products/addbrand.html')


@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == "POST":
        flash(f'The category {updatecategory.name} was changed to {category}', 'success')
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title='Update category', updatecategory=updatecategory)


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

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

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)

    brand = request.form.get('brand')
    category = request.form.get('category')

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.color = form.color.data
        product.description = form.description.data
        product.brand_id = request.form.get('brand')
        product.category_id = request.form.get('category')

        flash('The product was updated', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description

    return render_template('products/updateproduct.html', form=form, title='Update Product', product=product,
                           brands=brands, categories=categories)