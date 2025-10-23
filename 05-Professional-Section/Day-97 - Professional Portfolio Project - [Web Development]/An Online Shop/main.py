import os
import stripe
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
from flask import make_response
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Stripe configuration
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')

db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    stripe_payment_intent = db.Column(db.String(100))
    order_items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Routes
@app.route('/')
def index():
    featured_products = Product.query.limit(4).all()
    return render_template('index.html', products=featured_products)


@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('products'))

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    session['cart'] = cart
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        cart = session['cart']
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        if str(product_id) in cart:
            del cart[str(product_id)]
            session['cart'] = cart
            flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/checkout')
@login_required
def checkout():
    cart_items = []
    total = 0
    if 'cart' in session and session['cart']:
        cart = session['cart']
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
    else:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))

    return render_template('checkout.html', cart_items=cart_items, total=total,
                           stripe_public_key=stripe_public_key)


@app.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    try:
        # Calculate order total from cart
        total = 0
        if 'cart' in session:
            cart = session['cart']
            for product_id, quantity in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    total += product.price * quantity

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Convert to cents
            currency='usd',
            metadata={'user_id': session['user_id']}
        )

        return jsonify({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/payment-success')
@login_required
def payment_success():
    # Create order in database
    if 'cart' in session and session['cart']:
        cart = session['cart']
        total = 0
        order = Order(user_id=session['user_id'], total=0)
        db.session.add(order)
        db.session.flush()  # To get the order ID

        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total += item_total
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)

        order.total = total
        db.session.commit()

        # Clear cart
        session.pop('cart', None)

        flash('Payment successful! Thank you for your order.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('No items in cart.', 'warning')
        return redirect(url_for('cart'))


@app.route('/payment-cancelled')
def payment_cancelled():
    flash('Payment was cancelled.', 'warning')
    return redirect(url_for('cart'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.id.desc()).all()
    return render_template('dashboard.html', orders=user_orders)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Here you would typically save to database or send email
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/static/images/<filename>')
def serve_image(filename):
    try:
        # Try to serve the actual image
        return app.send_static_file(f'images/{filename}')
    except:
        # If image doesn't exist, return a placeholder
        placeholder_url = f"https://picsum.photos/500/500?random={hash(filename) % 100}"
        response = requests.get(placeholder_url)
        return make_response(response.content), 200, {'Content-Type': 'image/jpeg'}


# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    # Add sample products if none exist
    if not Product.query.first():
        sample_products = [
            Product(
                name="Premium T-Shirt",
                price=29.99,
                description="High-quality cotton t-shirt with a comfortable fit. Perfect for everyday wear.",
                image_url="/static/images/tshirt.jpg",
                stock=50
            ),
            Product(
                name="Classic Jeans",
                price=59.99,
                description="Durable denim jeans with a classic fit. Suitable for all occasions.",
                image_url="/static/images/jeans.jpg",
                stock=30
            ),
            Product(
                name="Running Shoes",
                price=89.99,
                description="Lightweight running shoes with excellent cushioning and support.",
                image_url="/static/images/shoes.jpg",
                stock=25
            ),
            Product(
                name="Winter Jacket",
                price=129.99,
                description="Warm and waterproof winter jacket with insulation for cold weather.",
                image_url="/static/images/jacket.jpg",
                stock=20
            )
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
