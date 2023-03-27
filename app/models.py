from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Phone(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    addresses = db.relationship('Address', backref='phone')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Phone {self.id}|{self.phone_number}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)


@login.user_loader
def get_a_phone_by_id(phone_id):
    return db.session.get(Phone, phone_id)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id')) 
    # SQL - FOREIGN KEY(user_id) REFERENCES user(id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id}|{self.state} {self.city} - {self.street_name} {self.number}>"
