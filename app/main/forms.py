from app.models import Pitch
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class post(FlaskForm):
    post = TextAreaField('Post', validators=[Required()])
    submit = SubmitField('post')