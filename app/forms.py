from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import validators


def validate_url(form, field):
    url = field.data.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not validators.url(url):
        raise ValidationError(
            "Please enter a valid URL (e.g., example.com or https://example.com)"
        )


class URLForm(FlaskForm):
    url = StringField(
        "Enter a website URL to count its words",
        validators=[DataRequired(), validate_url],
    )
    submit = SubmitField("Count Words")
