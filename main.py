from flask import Flask, render_template
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_product')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
# when upload on server set False






