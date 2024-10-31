from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


class URLForm(FlaskForm):
    url = StringField("Enter a website URL to count its words", validators=[DataRequired(), URL()])
    submit = SubmitField("Count Words")
