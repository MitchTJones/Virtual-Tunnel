from app.models import User, Organization
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, HiddenField, SelectMultipleField, widgets
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
    data = [('Black Student Union','Black Student Union'), ('Ultimate Frisbee','Ultimate Frisbee'), ('Creative Arts Club','Creative Arts Club'), ('SDT Sorority','SDT Sorority')]
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
    description = TextAreaField('Description', validators=[DataRequired()])
    org = HiddenField('Organization')
    art = HiddenField('Artwork')
    submit = SubmitField('Publish')
