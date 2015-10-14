from flask import render_template, redirect, request, \
    url_for, flash
from flask.ext.login import login_user, logout_user, login_required,\
    current_user
from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db
from ..models import User
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        print('{}未验证。'.format(current_user.username))
        return redirect(url_for('auth.unconfirmed'))


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
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Acount',
                   'auth/email/confirm', user=user, token=token)
#        except Exception as e:
#            print('出错了：', e)
#            db.session.delete(user)
#            flash('服务器出错了，玩会在场尝试～')
#            return render_template('auth/register.html', form=form)
        flash('A confirmation email has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@login_required
@auth.route('/confirm/<token>')
def confirm():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You hava confired your acount.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@login_required
@auth.route('/confirm')
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))
