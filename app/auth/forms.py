from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(form):
    email = StringField('Email', validators=[Required(), Lenth(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    rember_me = BooleanField('Keep me loggin in')
    submit = submit(Log In)
