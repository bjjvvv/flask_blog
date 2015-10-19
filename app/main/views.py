from flask import render_template, abort
from  ..models import User
from . import main

# 修饰器由蓝本提供
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.quey.filter_by(usernae=username).first_or_404()
    return render_template('user.html', user=user)
