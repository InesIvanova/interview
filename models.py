from app import db
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.username} {self.first_name} {self.last_name} "

    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'contact_emails': [mail.serialize for mail in self.contact_emails]
        }


class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(EmailType)
    contact_id = db.Column(db.Integer, ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    contact = relationship('Contact', backref='contact_emails', foreign_keys=[contact_id])

    def __init__(self, email, contact_id):
        self.email = email
        self.contact_id = contact_id

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'email': self.email,
            'contact_id': self.contact_id
        }