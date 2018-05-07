from app import db, login_manager
from flask_login import UserMixin

followers = db.Table('follower',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followee_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)

    # back reference in User that points to Shoutout
    shoutous = db.relationship('Shoutout', backref='user', lazy='dynamic')

    following = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followee_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

class Shoutout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
