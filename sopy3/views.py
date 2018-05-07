from app import app, photos, db
from models import User, Shoutout
from forms import RegisterForm, LoginForm, ShoutoutForm
from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_required, login_user, current_user, logout_user

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
    form = ShoutoutForm()

    user_id = current_user.id
    shoutouts = Shoutout.query.filter_by(user_id=user_id).order_by(Shoutout.date_created.desc()).all() # order by most recent shoutout

    current_time = datetime.now()


    return render_template('timeline.html', form=form, shoutouts=shoutouts, current_time=current_time)

@app.route('/post_shoutout', methods=['POST'])
@login_required
def post_shoutout():
    form = ShoutoutForm()

    if form.validate():
        shoutout = Shoutout(user_id=current_user.id, text=form.text.data, date_created=datetime.now())
        db.session.add(shoutout)
        db.session.commit()
        return redirect(url_for('timeline'))

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
