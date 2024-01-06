"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

@app.route('/')
def welcome():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def user_form():
    return render_template('create-user-form.html')

@app.route('/users/new',methods = ['POST'])
def creating_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def details(user_id):
    user = User.query.get(user_id)
    return render_template('detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get(user_id)
    return render_template('edit-user-form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    new_first_name = request.form['first_name']
    new_last_name = request.form['last_name']
    new_image_url = request.form['image_url']
    user = User.query.get(user_id)
    if new_first_name:
        user.first_name = new_first_name 
    if new_last_name:
        user.last_name = new_last_name 
    if new_image_url:
        user.image_url = new_image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>/delete')
def delete(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')