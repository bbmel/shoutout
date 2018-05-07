from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('full name required'), Length(max=100, message='Name cannot exceed 100 characters.')])
    username = StringField('Username', validators=[InputRequired('username required'), Length(max=100, message='Username cannot exceed 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('password required')])
    image = FileField(validators=[FileAllowed(IMAGES, 'only images allowed')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('username required'), Length(max=100, message='Username cannot exceed 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('password required')])
    remember = BooleanField('Remember me')

class ShoutoutForm(FlaskForm):
    text = TextAreaField('Shoutout', validators=[InputRequired('shoutout required')])
