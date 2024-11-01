from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

def validate_url(form, field):
    pattern = r'^(https?:\/\/)?[\w\-]+(\.[\w\-]+)+[/#?]?.*$'
    if not re.match(pattern, field.data.strip()):
        raise ValidationError('Invalid URL format')

class URLForm(FlaskForm):
    url = StringField("Enter a website URL to count its words", 
                     validators=[DataRequired(), validate_url])
    submit = SubmitField("Count Words")
