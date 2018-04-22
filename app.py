from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField
from wtforms.validators import InputRequired, Length


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mgravier/Desktop/shoutout/shoutout.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'sdakfjhddsaklfjhdfjhjkcdksajfhab'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))

class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name is required.'), Length(max=100, message='Name cannot exceed 100 characters.')])
    username = StringField('Username', validators=[InputRequired('A username is required.'), Length(max=100, message='Username cannot exceed 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('A full name is required.')])
    image = FileField()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    manager.run()
