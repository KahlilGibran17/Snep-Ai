from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=32)])