from dataclasses import dataclass
from flask_bcrypt import generate_password_hash, check_password_hash
from .db import db

from datetime import datetime

@dataclass
class User(db.Model):
    __tablename__ = "users_user"

    '''Declare static to avoid {} objects'''
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    created: datetime
    last_updated: datetime

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    last_updated = db.Column(db.DateTime, onupdate=datetime.now())
    upload = db.relationship('Upload', cascade="all,delete", backref='users_user')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

@dataclass
class Upload(db.Model):
    __tablename__ = "users_uploads"
    '''Declare static to avoid {} objects'''
    id:int
    state:str
    user_id:int
    created: datetime

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    created = db.Column(db.DateTime, default=datetime.now())
    location = db.relationship('Location', cascade="all,delete", backref='users_uploads', uselist=False)

@dataclass
class Location(db.Model):
    __tablename__ = "uploads_location"
    '''Declare static to avoid {} objects'''
    id: int
    lat: float
    long: float
    type: str
    upload_id: int

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    type = db.Column(db.String)
    upload_id = db.Column(db.Integer, db.ForeignKey('users_uploads.id'))

