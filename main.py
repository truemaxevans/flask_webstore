from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mystore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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


if __name__ == '__main__':
    app.run(debug=True)
# when upload on server set False
