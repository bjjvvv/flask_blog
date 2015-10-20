from flask import render_template, abort, flash, redirect, \
    url_for
from flask.ext.login import current_user
from .. import db
from  ..models import User
from . import main
from .forms import EditProfileFrom

# 修饰器由蓝本提供
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.quey.filter_by(usernae=username).first_or_404()
    return render_template('user.html', user=user)

def edit_profile():
    form = EditProfileFrom()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.seesion.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location = current_user.location
    form.about_me = current_user.about_me
    return render_template('edit_profile.html', form=form)
