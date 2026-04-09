# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired,Length
from flask_wtf.file import FileRequired, FileAllowed

class MovieForm(FlaskForm):
    title = StringField("Movie title", validators=[InputRequired(), Length(min=1, max=100, message="Must be between 1 and 100 characters")])
    description = TextAreaField("Movie description", validators=[InputRequired(), Length(min=1, max=500, message="Must be between 1 and 500 characters")])
    poster = FileField("Movie Poster", validators=[FileRequired(message="Please choose a file"), FileAllowed({'jpg', 'png', 'webp'}, message="Only .webp, .jpg and .png files allowed")])