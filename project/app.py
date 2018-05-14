from flask import Flask, render_template, redirect, url_for, request, flash
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length
from models import *
from flask_login import login_user, current_user, logout_user, LoginManager

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

@app.route('/est')
def est():
    ests = Establishment.query.all()
    return render_template('est.html', ests=ests)

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


@app.route('/est/<int:id_est>')
def estId(id_est):
    assorts = Assortments.query.filter_by(id_establishment=id_est)
    return render_template('showAssorts.html', assorts=assorts)

if __name__ == '__main__':
    app.run(debug=True)
