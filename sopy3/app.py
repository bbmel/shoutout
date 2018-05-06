from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime


app = Flask(__name__)


app.config['UPLOADED_PHOTOS_DEST'] = '/Users/mgravier/Desktop/shoutout/sopy3/images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mgravier/Desktop/shoutout/sopy3/shoutout.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'sdakfjhddsaklfjhdfjhjkcdksajfhab'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)

class Shoutout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = name = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('full name required'), Length(max=100, message='Name cannot exceed 100 characters.')])
    username = StringField('Username', validators=[InputRequired('username required'), Length(max=100, message='Username cannot exceed 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('password required')])
    image = FileField(validators=[FileAllowed(IMAGES, 'only images allowed')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('username required'), Length(max=100, message='Username cannot exceed 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('password required')])
    remember = BooleanField('Remember me')


@app.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # verify user and pw
        if not user:
            return render_template('index.html', form=form, message='Login failed for {}'.format(form.username.data))

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('profile'))

        return render_template('index.html', form=form, message='Login failed for {}'.format(form.username.data))
    # if the form isn't validated
    return render_template('index.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)

        new_user = User(name=form.name.data, username=form.username.data, image=image_url, password=generate_password_hash(form.password.data), join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    manager.run()
