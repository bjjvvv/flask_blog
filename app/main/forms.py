from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import Length


class EditProfileFrom(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextField('About me')
    submit = SubmitField('Submit')
