from flask import Flask, render_template, redirect, url_for, request, flash
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length
from models import *
from flask_login import login_user, current_user, logout_user, LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import psycopg2
from datetime import datetime
from random import randint


app = Flask(__name__)
app.config['SECRET_KEY'] = "this_is_secret"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://almaz:Almaz@localhost/diamond'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin(app)

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

#Forms
class LoginForm(FlaskForm):
    number = IntegerField('Mobile number', validators = [InputRequired()])
    password = PasswordField('Пароль', validators = [InputRequired(),
                                                        Length(min=4, max=80)])

class RegForm(FlaskForm):
    number = IntegerField('Mobile number', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(),
                        Email(message = 'Не правилный email'), Length(max=50)])
    password = PasswordField('Пароль',
                         validators = [InputRequired(), Length(min=4, max=80)])

class UpdateAccountForm(FlaskForm):
    first = StringField('First name')
    last = StringField('Last name')


    submit = SubmitField('Submit')


#Routes
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/food/<int:id_cuisine>')
def foodCuisine(id_cuisine):
    # cuisine = CuisineofEstablishment.query.filter_by(id=id_cuisine)
    # return render_template('showEstById_Cuisine.html', cuisine=cuisine)
    return redirect(url_for('est'))

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    form = RegForm()

    if form.validate_on_submit():
        new_user = Client(mobile_number=form.number.data, email=form.email.data,
                                                    password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("You are succesfully registred!")

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Client.query.filter_by(mobile_number=form.number.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dash'))
        return '<h1>Invalid username or password.</h1>'
    return render_template('login.html', form=form)

@app.route('/dash')
def dash():
    return render_template('dash.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first = form.first.data
        current_user.last = form.last.data

        db.session.commit()

        flash('Your account has been updated!')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first.data = current_user.first
        form.last.data = current_user.last

    return render_template('account.html', title='Account', form=form)

@app.route('/est')
def est():
    ests = Establishment.query.all()
    return render_template('est.html', ests=ests)

@app.route('/est/<int:id_est>', methods=['GET', 'POST'])
def estId(id_est):
    if request.method == 'POST':
        price = request.form.get('order')
        subId = Subsidiary.query.filter_by(id_establishment=id_est).first()
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rand = randint(1000, 9999)

        new_order = Order(
            dateAndTime_of_order=cur_time,
            id_client=current_user.id, id_subsidiary=subId.id, total_price=price,
            order_issued=False, confirmation_code=rand
            )

        db.session.add(new_order)
        db.session.commit()
        return render_template('ordered.html', order=new_order)
    else:
        assorts = Assortments.query.filter_by(id_establishment=id_est)
        return render_template('showAssorts.html', assorts=assorts)


#Admin view
admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderOfAssortment, db.session))
admin.add_view(ModelView(Subsidiary, db.session))
admin.add_view(ModelView(CategoryAssortment, db.session))
admin.add_view(ModelView(Assortments, db.session))
admin.add_view(ModelView(Establishment, db.session))
admin.add_view(ModelView(Cuisine, db.session))
admin.add_view(ModelView(CuisineofEstablishment, db.session))

if __name__ == '__main__':
    app.run(debug=True)
