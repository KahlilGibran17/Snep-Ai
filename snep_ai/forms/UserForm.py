from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo
from snep_ai.models.User import User

class CreateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=32), EqualTo('confirm_password', message="Field must be equal to Confirm Password.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=32)])
    role = RadioField('Role', choices=[("true", "Admin"), ("false", "User")], default="true", validators=[InputRequired()])

class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('New Password', validators=[EqualTo('confirm_password', message="Field must be equal to Confirm Password.")])
    confirm_password = PasswordField('Confirm New Password')