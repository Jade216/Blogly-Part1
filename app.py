"""Blogly application."""

from flask import Flask, redirect, request, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users = users)

@app.route('/users/new')
def users_new_form():
    '''show a form to create a new user'''
    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def add_new():
    ''''handle submission for creating new user'''
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_info(user_id):
    '''specific user's info page'''
    user = User.query.get_or_404(user_id)
    return render_template('info.html', user = user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    '''edit page for user'''
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def users_update(user_id):
    '''update users after edit'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def users_delete(user_id):
    '''delete an user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')