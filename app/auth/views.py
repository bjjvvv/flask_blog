from flask import render_template, redirect, request, \
    url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db
from ..models import User
from ..email import send_email


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
    logout_user()
    flash('You have benn loged out.')
    return redirect(url_for('main.index'))

@login_required
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return True
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Acount', 
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
