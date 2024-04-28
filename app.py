from flask import Flask, render_template, request, redirect, url_for, flash , jsonify
from wtforms import  StringField, validators ,PasswordField , BooleanField ,SelectField , SubmitField
from flask_wtf import FlaskForm
import requests
from flask_sqlalchemy import SQLAlchemy , pagination
from flask import Flask, session
from flask_session import Session
import subprocess
import datetime
from flask_paginate import Pagination



import datetime

SECONDS_PER_DAY = 86400
SECTIONS = 4
SECONDS_PER_SECTION = SECONDS_PER_DAY // SECTIONS

current_time = datetime.datetime.now().time()

hours, minutes= current_time.hour, current_time.minute

total_seconds = (hours * 3600) + (minutes * 60)

if total_seconds < SECONDS_PER_SECTION:
    section = 1
elif total_seconds < SECONDS_PER_SECTION * 2:
    section = 2
elif total_seconds < SECONDS_PER_SECTION * 3:
    section = 3
else:
    section = 4

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['PER_PAGE'] = 9


Session(app)

db = SQLAlchemy(app)

class SignupForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired(message="Enter correct Email Address")])
    password = PasswordField('Password', [
        validators.DataRequired(message='Please enter a password.'),
        validators.Length(min=8, message='Your password must be at least 8 characters long.'),
        validators.EqualTo('re_password', message='Passwords must match')
    ])
    re_password = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class SpecialtyForm(FlaskForm):
    specialty = SelectField('specialty',choices=['General Physician','ENT'])
    submit = SubmitField('submit')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return '<Patient %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    re_password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

class doctorlist(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(80), nullable=False)
    expertise = db.Column(db.String(120), unique=True, nullable=False)
    hospital_name = db.Column(db.String(10), nullable=False)
    availablity = db.Column(db.Integer, nullable=False)
   
    def __repr__(self):
        return '<Doctor %r>' % self.doctor_name

class medicinelist(db.Model):
    medicine_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availablity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(80), nullable=False)
   
    def __repr__(self):
        return '<Medicine %r>' % self.medicine_name

class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], Pagination(page=page, per_page=per_page, total=len(items))

@app.route('/')
def index():
    return render_template('new_index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        re_password = form.re_password.data
        user = User(username=username, email=email, password=password, re_password=re_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up! Please log in.')
        return redirect(url_for('login'))
    return render_template("signup.html", form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.password == password:
            session["logged_in"] = True
            session['user_id'] = user.id
            flash('You were successfully logged in')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    return render_template('newlogin.html',form=form)

@app.route('/dashboard')
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

@app.route("/pharmacy", methods = ['POST','GET'])
def pharmacy():
    page = request.args.get('page', 1, type=int)
    medicines = medicinelist.query.paginate(page=page, per_page=app.config['PER_PAGE'])
    cart = session.get('cart', {})
    return render_template('medicines.html',medicines = medicines , pagination = pagination , cart = cart)

@app.route("/filtered_medicine", methods = ['POST','GET'])
def filtered_medicine():
    if request.method == 'POST':
        med_name = request.form['medicine']
        filtered_medicines = db.session.query(medicinelist).filter_by(medicine_name=med_name).all()
    else:
        filtered_medicines = medicinelist.query.all()
    page = request.args.get('page', 1, type=int)
    medicines = paginate(filtered_medicines, page, app.config['PER_PAGE'])
    return render_template('medicines.html',medicines=medicines)

def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], Pagination(page=page, per_page=per_page, total=len(items))

@app.context_processor
def inject_pagination():
    return dict(Pagination=Pagination)

@app.route('/joininglink', endpoint='joininglink')
def index():
    return render_template('video_consult.html')

@app.route('/find_doctors')
def find_doctors():
    return render_template('find_doctors.html')

@app.route('/run_script', methods=['POST','GET'])
def run_script():
    subprocess.Popen(['python', 'D:\BCA_PROJECT\joning_link.py'])
    return render_template('timeslot.html')

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session.clear()
    return render_template('new_index.html')


@app.route('/profile')
def profile():
    if request.method == 'POST':
        session["logged_in"] = True
        user = User.query.first()
        user.username = request.form['name']
        user.address = request.form['address']
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
    user = User.query.first()
    return render_template('profile.html', user=user)

@app.route('/sos')
def sos():
    return render_template('sos.html')

@app.route('/bloodbank')
def bloodbank():
    return render_template('bloodbank.html')

@app.route('/videoconsult' , methods = ['POST','GET'])
def videoconsult():
    return render_template('new_video_consult.html')

@app.route('/timeslot' , methods = ['POST','GET'])
def timeslot():
    return render_template('timeslot.html')


@app.route('/result' , methods = ['POST','GET'])
def result():
    name = request.form['name']
    now = section

    if not name:
        flash('Please select an option.')
        return redirect(url_for('timeslot'))

    doctors = db.session.query(doctorlist).filter_by(expertise=name).filter(doctorlist.availablity == now).all()
    return render_template('result.html', doctors=doctors)

@app.route('/add_to_cart/<medicine_id>' , methods = ['POST','GET'])
def add_to_cart(medicine_id):

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
    else:
        quantity = int(request.args.get('quantity', 1))

    medicine = medicinelist.query.get(medicine_id)

    cart = session.get('cart', {})

    # Check if item already exists in cart
    if 'cart' in session and str(medicine_id) in session['cart']:
        session['cart'][str(medicine_id)]['quantity'] += quantity
        session['cart'][str(medicine_id)]['price'] += medicine.price * quantity
    else:
        session.setdefault('cart', {})
        session['cart'][str(medicine_id)] = {
            'name': medicine.medicine_name,
            'quantity': quantity,
            'price': medicine.price * quantity
        }

    session['cart'] = cart    

    return redirect('/cart')


@app.route('/update_cart/<int:medicine_id>', methods=['POST'])
def update_cart(medicine_id):
    quantity = int(request.form['quantity'])
    cart = session.get('cart', {})
    cart[medicine_id] = quantity
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})

    total_price = 0
    for medicine_id, medicine in cart.items():
        total_price += medicine['price'] * medicine['quantity']
        session['total_price'] = total_price

    render_template('cart.html', cart=cart, total_price=total_price)

    return redirect(url_for('pharmacy'))

@app.route('/viewcart')
def viewcart():
    cart = session.get('cart', {})

    total_price = 0    
    for medicine_id, medicine in cart.items():
        total_price += medicine['price'] * medicine['quantity']


    render_template('cart.html', cart=cart, total_price=total_price)

    return render_template('cart.html',cart=cart, total_price = total_price)

@app.route('/remove_from_cart/<medicine_id>' , methods = ['POST','GET'])
def remove_from_cart(medicine_id):
    if 'cart' not in session:
        session['cart'] = {}

    if medicine_id in session['cart']:
        total_price = session.get('total_price', 0)
        medicine_price = session['cart'][medicine_id]['price']
        total_price -= medicine_price
        session['total_price'] = total_price

        del session['cart'][medicine_id]

    return redirect('/cart')



if __name__ == '__main__':
    app.run(debug=True)
