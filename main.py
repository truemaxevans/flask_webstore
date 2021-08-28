from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mystore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'secret'
app.config["CSRF_ENABLED"] = True
app.config["USER_ENABLE_EMAIL"] = False

db = SQLAlchemy(app)

admin = Admin(app, name='Admin', template_mode='bootstrap3')
# Flask users


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')


user_manager = UserManager(app, db, User)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # auto +1
    title = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)

    # show title for added positions
    def __repr__(self):
        return self.title


@app.route('/')
def index():
    # Show all products ordered by price
    products = Product.query.order_by(Product.price).all()
    return render_template('index.html', data=products)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_product', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        product = Product(title=title, price=price, description=description)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'

    else:
        return render_template('create.html')


@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error, try again'
    else:
        return render_template('registration.html')


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))


if __name__ == '__main__':
    app.run(debug=True)
# when upload on server set False
