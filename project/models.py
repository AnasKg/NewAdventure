from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin, LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "this_is_secret"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://almaz:Almaz@localhost/diamond'
modus = Modus(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

#DB models
class Client(UserMixin, db.Model):
    #db.Columns
    __tablename__ = "Client"
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Text)
    last = db.Column(db.Text)
    username = db.Column(db.Text)
    personal_account = db.Column(db.Integer)
    password = db.Column(db.Text)
    mobile_number = db.Column(db.Integer)
    email = db.Column(db.Text)
    block_user = db.Column(db.Boolean)

    #relationships
    order = db.relationship('Order', backref='client')


class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('Client.id')) #ForeignKey
    id_subsidiary = db.Column(db.Integer, db.ForeignKey('Subsidiary.id')) #ForeignKey
    dateAndTime_of_order = db.Column(db.DateTime)
    total_price = db.Column(db.Float)
    order_issued = db.Column(db.Boolean)
    confirmation_code = db.Column(db.Integer)

    #relationships
    orderOfAssortment = db.relationship('OrderOfAssortment', backref='order')

class OrderOfAssortment(db.Model):
    __tablename__ = "Order_Of_Assortment"
    id = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('Order.id')) #ForeignKey
    id_assortment = db.Column(db.Integer, db.ForeignKey('Assortments.id'))
    amount = db.Column(db.Integer)
    price_of_order = db.Column(db.Float)

class Subsidiary(db.Model):
    __tablename__ = "Subsidiary"
    id = db.Column(db.Integer, primary_key=True)
    id_establishment = db.Column(db.Integer, db.ForeignKey('Establishment.id')) #ForeignKey
    title_subsidiary = db.Column(db.Text)
    lat = db.Column(db.Numeric)
    lon = db.Column(db.Numeric)
    address = db.Column(db.Text)
    mobile_number = db.Column(db.Integer)
    login = db.Column(db.Text)
    password = db.Column(db.Text)

    #relationships
    order = db.relationship('Order', backref='subsidiary')

class CategoryAssortment(db.Model):
    __tablename__ = "Category_Assortment"
    id = db.Column(db.Integer, primary_key=True)
    title_Category_Assortment = db.Column(db.Text)

    #relationship
    assortment = db.relationship('Assortments', backref='catAssortment')

class Assortments(db.Model):
    __tablename__ = "Assortments"
    id = db.Column(db.Integer, primary_key=True)
    id_establishment = db.Column(db.Integer, db.ForeignKey('Establishment.id')) #ForeignKey
    title_assortment = db.Column(db.Text)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    id_cuisine = db.Column(db.Integer, db.ForeignKey('Cuisine.id')) #ForeignKey
    id_category_assortment = db.Column(db.Integer, db.ForeignKey('Category_Assortment.id'))#ForeignKey

    #relationships
    orderOfAssortment = db.relationship('OrderOfAssortment', backref='assortments')

class Establishment(db.Model):
    __tablename__ = "Establishment"
    id = db.Column(db.Integer, primary_key=True)
    title_establishment = db.Column(db.Text)
    mobile_number = db.Column(db.Integer)
    email = db.Column(db.Text)
    login = db.Column(db.Text)
    password = db.Column(db.Text)
    account = db.Column(db.Integer)
    lat = db.Column(db.Numeric)
    lon = db.Column(db.Numeric)
    address = db.Column(db.Text)

    #relationships
    subsidiary = db.relationship('Subsidiary', backref='establishment')
    assortment = db.relationship('Assortments', backref='establishment')
    cuisineOfEst = db.relationship('CuisineofEstablishment', backref='establishment')


class Cuisine(db.Model):
    __tablename__ = "Cuisine"
    id = db.Column(db.Integer, primary_key=True)
    title_cuisine = db.Column(db.Text)
    description = db.Column(db.Text)

    #relationship
    assortment = db.relationship('Assortments', backref='cuisine')
    cuisine = db.relationship('CuisineofEstablishment', backref='cuisine')


class CuisineofEstablishment(db.Model):
    __tablename__ = "Cuisine_of_Est"
    id = db.Column(db.Integer, primary_key=True)
    id_establishment = db.Column(db.Integer, db.ForeignKey('Establishment.id'))#ForeignKey
    id_cuisine = db.Column(db.Integer, db.ForeignKey('Cuisine.id'))

if __name__ == '__main__':
    app.run(debug=True)
