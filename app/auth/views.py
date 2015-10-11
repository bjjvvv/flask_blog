from flask import render_template, redirect, request, \
    url_for, flash
from flask.ext.login import login_user, login_required
from ..models import User
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rember_me.data)
            return redirect(request.args.get('next') or
                    url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

@login_required
@auth.route('/logout')
def logout():
    login_user()
    flash('You have benn loged out.')
    return redirect(url_for('main.index'))
