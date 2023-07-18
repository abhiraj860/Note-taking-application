from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    day = db.Column(db.String(10), default=datetime.now().strftime('%A'))
    currDate = db.Column(db.String(20), default=datetime.now().strftime('%Y-%m-%d'))
    time = db.Column(db.String(20), default=datetime.now().strftime('%H:%M:%S'))
    month = db.Column(db.String(20), default=datetime.now().strftime('%B'))
    sentiment = db.Column(db.Float)
    sentimentColor = db.Column(db.String(255))
    classification = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
