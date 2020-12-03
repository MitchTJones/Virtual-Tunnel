from flask import render_template, request, url_for, redirect, flash
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField,  widgets
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import text

app = Flask(__name__)
db = SQLAlchemy(app)
application = app
migrate = Migrate(app, db)
login = LoginManager(app)

##configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'hci-2020-hard-to-guess'
app.config["IMAGE_UPLOADS"] = 'static/uploads'

#running shell- can delete later
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Organization': Organization}


##Users DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    affiliated_org = db.relationship('Organization', backref='affiliations', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)


##Posts DB
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(140))
    description = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Post {}>'.format(self.description) 

##Organizations DB
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Organization {}>'.format(self.org) 


##Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    data = [('bsu','Black Student Union'), ('uf','Ultimate Frisbee'), ('cac','Creative Arts Club'), ('sdt','SDT Sorority')]
    orgs = SelectMultipleField('Select organizations', choices=data, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')




##Paths
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
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
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

@app.route('/paint')
def paint():
    return render_template('paint.html')

@app.route('/gallery')
def gallery():
    return render_template('view.html')

@app.route('/')
def index():
    if current_user.is_authenticated:
        orgs = Organization.query.filter_by(user_id=current_user.id)
        return render_template('home.html', orgs = orgs)
    else:
        return render_template('home.html')