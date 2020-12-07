from flask import Flask, render_template, request, flash, redirect
from app import app, db
from app.forms import LoginForm, RegistrationForm, SubmitForm
from app.models import User, Post, Organization
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

page = 'paintPage'

def flash_errors(form, type):
    for field, errors in form.errors.items():
        for error in errors:
            flash(type+error)
            return render_template('home.html', activePage = page, lform = LoginForm(), sform = RegistrationForm(), uform = SubmitForm(), user = current_user)

@app.route('/')
def index():
    orgs = False
    if current_user.is_authenticated:
        orgs = Organization.query.filter_by(user_id=current_user.id)
        return render_template('home.html', activePage = page, lform = LoginForm(), sform = RegistrationForm(), uform = SubmitForm(), user = current_user, orgs = orgs)
    return render_template('home.html', activePage = page, lform = LoginForm(), sform = RegistrationForm(), uform = SubmitForm(), user = current_user)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        username = form.username.data
        new_user.set_password(form.password.data)
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash('`Username taken')
            return redirect('/')
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash('`That email is already associated with an account.')
            return redirect('/')
        db.session.add(new_user)
        db.session.commit()
        registered_user = User.query.filter_by(username=username).first()
        user_id = registered_user.id
        orglist =  form.orgs.data
        print(orglist)
        print(user_id)
        for org in orglist:
            new_org_entry = Organization(user_id = user_id, org = org)
            db.session.add(new_org_entry)
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
            print("HELLO")
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

@app.route('/submit', methods=['POST'])
def submit():
    if not current_user.is_authenticated:
        print("ouch")
        flash('-You must be logged in to submit your artwork!')
        return redirect('/')
    form = SubmitForm()
    if form.validate_on_submit():
        print('hi')
        # TODO: submission back-end
    flash('|Artwork Submitted')
    return redirect('/')