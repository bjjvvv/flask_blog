from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
Email()])
    password = PasswordField('Password', validators=[Required()])
    rember_me = BooleanField('Keep me loggin in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[a-zA-Z][a-zA-Z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores'
                                          )])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(),
        EqualTo('password2', 'Passwors must match')])
    password2 = PasswordField('New password', validators=[Required()])
    submit = SubmitField('Update password')


class PassowrdResetRequestFrom(Form):
    email = StringField('Your Email', validators=[Required(), Length(1,64),
                                                              Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Your Email', validators=[Required(), Length(1,64),
                                                              Email()])
    password = PasswordField('New password', validators=[Required(),
        EqualTo('password2', 'Passwors must match')])
    password2 = PasswordField('New password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validator_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknow email address.')
