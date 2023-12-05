from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username: ", validators=[Length(min=3, max=120), DataRequired()], name='username')
    email = StringField("Email: ", validators=[Length(min=10, max=120), Email()], name='email')
    password = PasswordField("Email: ", validators=[Length(min=8, max=25), EqualTo("repeat_password")], name='password')
    repeat_password = PasswordField("Email: ", validators=[Length(min=8, max=25)], name='repeat_password')


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()], name='username')
    password = PasswordField("Email: ", validators=[Length(min=8), EqualTo("repeat_password")], name='password')