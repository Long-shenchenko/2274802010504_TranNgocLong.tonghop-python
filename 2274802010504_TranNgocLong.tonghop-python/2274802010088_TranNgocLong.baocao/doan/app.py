from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import locale

# Khởi tạo ứng dụng Flask
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

app.secret_key = 'your_secret_key'  # Bảo mật session

# Cấu hình kết nối đến PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ngoclong@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Đặt định dạng ngôn ngữ cho VN
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

# Định nghĩa model cho sản phẩm
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

# Định nghĩa model cho đơn hàng
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100))
    ward = db.Column(db.String(100))
    city = db.Column(db.String(100))
    total_amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Định nghĩa model cho mục đơn hàng
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

# Hàm định dạng số cho template Jinja2
def number_format(value, decimal_places=0, decimal_point=',', thousands_sep='.'):
    if value is None:
        return ''
    formatted_value = f"{value:,.{decimal_places}f}".replace(',', 'X').replace('.', decimal_point).replace('X', thousands_sep)
    return formatted_value

# Đăng ký hàm định dạng với Jinja2
app.jinja_env.filters['number_format'] = number_format

# Route trang chủ
@app.route('/')
def index():
    products = Product.query.all()
    cart_items = session.get('cart', [])
    cart_count = sum(item.get('quantity', 0) for item in cart_items)
    return render_template('index.html', products=products, cart_count=cart_count)

# Thêm sản phẩm vào giỏ hàng
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if 'cart' not in session:
        session['cart'] = []
    existing_product = next((item for item in session['cart'] if item['id'] == product_id), None)
    if existing_product:
        existing_product['quantity'] += 1
    else:
        session['cart'].append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        })
    session.modified = True
    return redirect(url_for('index'))

# Route giỏ hàng
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        for item in session.get('cart', []):
            quantity = request.form.get(f'quantity_{item["id"]}', 1)
            item['quantity'] = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

# Xóa sản phẩm khỏi giỏ hàng
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    return redirect(url_for('cart'))

# Route thanh toán
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart_items = session.get('cart', [])
        total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        order = Order(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            district=request.form.get('district'),
            ward=request.form.get('ward'),
            city=request.form.get('city'),
            total_amount=total
        )
        db.session.add(order)
        db.session.flush()
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        db.session.commit()
        session['cart'] = []
        return redirect(url_for('payment'))
    return render_template('checkout.html')

# Route trang thanh toán
@app.route('/payment')
def payment():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    return render_template('payment.html', cart=cart_items, total=total)

# Khởi tạo database và thêm sản phẩm mẫu
def init_db():
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            products = [
                Product(name="Áo Gucci", price=22000000),
                Product(name="Quần Gucci", price=15000000),
                Product(name="Giày Gucci", price=20000000),
                Product(name="Áo thun Gucci", price=12000000),
                Product(name="quần short Gucci", price=5500000),
                Product(name="wallet Gucci", price=7000000),
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
            print("Đã khởi tạo database và thêm dữ liệu mẫu!")
        else:
            print("Database đã có dữ liệu!")
# Chạy ứng dụng
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
