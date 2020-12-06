from flask import Flask, render_template, request, flash, redirect
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post, Organization
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

page = 'paintPage'

@app.route('/')
def index():
    uform = UploadForm() 
    if uform.validate_on_submit():
        uploaded_file = uform.file.data #Make sure you're feeding the image file into this field with a filename
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config["IMAGE_UPLOADS"], uploaded_file.filename)) #image stored in static/uploads
            user_id = current_user.id
            description = uform.description.data
            org = uform.organization.data #from list of user orgs
            new_post = Post(filename=uploaded_file.filename, org = org, description = description, user_id = user_id)
            try:
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('gallery')) ##Where gallery goes
            except:
                print(filename)
                return "error"
    return render_template('home.html', activePage = page, lform = LoginForm(), sform = RegistrationForm(), user = current_user)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/gallery')
def gallery():
    posts = Post.query.order_by(Post.timestamp)
    return render_template('gallery.html', posts =posts) #use posts for jinja2 templates

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        # if User.query.filter_by(username=form.username.data).first() is not None:
        #     flash('`Username taken')
        #     return redirect('/')
        # if User.query.filter_by(email=form.email.data).first() is not None:
        #     flash('`That email is already associated with a MeetUp account.')
        #     return redirect('/')
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('~Account ' + form.username.data + ' Created.')
        return redirect('/')
    else:
        flash_errors(form, '`')
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('`Wrong Username or Password')
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    else:
        flash('`Wrong Username or Password')
    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
