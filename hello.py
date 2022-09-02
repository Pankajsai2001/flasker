from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
from datetime import datetime



app=Flask(__name__)
# secret key
app.config['SECRET_KEY']="my secret key"
# add database #sqlite
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# Mysql 
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Accolite!368@localhost/our_users'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Accolite@368'
# app.config['MYSQL_DB'] = 'flask'

# Initialieze The Database
db = SQLAlchemy(app)
# db = MySQL(app)

# create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name
 
# Create a Users Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create form class
class NamerForm(FlaskForm):
    name = StringField("What's Your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()


@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first() 
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added) 

    return render_template("add_user.html",form=form,name=name,our_users=our_users)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    # li=['pankaj','sai','majji']
    return render_template("user.html",name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name= form.name.data
        form.name.data=''
        flash("Form Sumnitted Succesfully")

    return render_template('name.html',
    name=name,
    form = form)