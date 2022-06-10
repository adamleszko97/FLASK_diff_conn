from . import db
from flask_login import UserMixin
from . import login
from sqlalchemy import Column, String, Integer, VARCHAR, BigInteger


class users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.VARCHAR(45), unique=True)
    password = db.Column(db.VARCHAR(45))

class employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(45))
    last_name = db.Column(db.VARCHAR(45))
    phone_number = db.Column(db.BigInteger)
    department = db.Column(db.VARCHAR(45))

@login.user_loader
def load_user(id):
    return users.query.get(int(id))

