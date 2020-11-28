from flask import render_template
from app import app

@app.route('/')
def index():
    user = {'username': 'Bob Smitherson'}
    return render_template('home.html', user=user)