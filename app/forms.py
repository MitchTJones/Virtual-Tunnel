from app.models import User, Organization
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo

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
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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

class SubmitForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    org = HiddenField('Organization')
    submit = SubmitField('Publish')
