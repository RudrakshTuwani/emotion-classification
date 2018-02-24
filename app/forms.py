from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, TextField
from wtforms.validators import URL, Optional


class ImageForm(FlaskForm):
    image = FileField(validators=[Optional()])
    url = TextField('URL', validators=[Optional(), URL()])
    submit = SubmitField('Submit')
