from flask_restful import Resource, request
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from flask_api import status, exceptions

from models import Contact, Email
from app import db
from app import celery

from datetime import datetime, timedelta
import random
import string


class ContactListCreateView(Resource):
    def get(self):
        if request.args:
            username = request.args.to_dict()['username']
            contact = Contact.query.filter_by(username=username).first()
            if contact:
                return jsonify({'contact': contact.serialize, 'message': 'OK', 'status': status.HTTP_200_OK})
            return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})
        contacts = Contact.query.all()
        return jsonify({'contacts': [result.serialize for result in contacts]})

    def post(self):
        if request.json:
            data = request.json
            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            contact = Contact(username=username, first_name=first_name, last_name=last_name)
            db.session.add(contact)

            try:
                db.session.commit()
            except SQLAlchemyError as ex:
                error = str(ex.__dict__['orig'])
                return jsonify({'message': error, 'status': status.HTTP_400_BAD_REQUEST})
            print(data.keys())
            if 'contact_emails' in data.keys():
                emails_names = data['contact_emails']
                for name in emails_names:
                    email = Email(email=name, contact_id=contact.id)
                    db.session.add(email)
                db.session.commit()

            return jsonify({'status': '201'})
        return jsonify({'message': 'Request data was not in a correct format', 'status': status.HTTP_400_BAD_REQUEST})


class ContactRetrieveUpdateDeleteView(Resource):
    def get(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            return jsonify({'contact': contact.serialize, 'message': 'OK', 'status': status.HTTP_200_OK})
        return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})

    def put(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            data = request.json
            contact.username = data['username']
            contact.first_name = data['first_name']
            contact.last_name = data['last_name']
            print(contact)
            db.session.commit()
            return jsonify({'message': 'Resource Updated Successfully', 'status': status.HTTP_200_OK})
        return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})

    def delete(self, id):
        contact = Contact.query.filter_by(id=id).first()
        emails = Email.query.filter_by(contact_id=id)
        [db.session.delete(mail) for mail in emails]
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({'message': 'No Content', 'status': status.HTTP_204_NO_CONTENT})
        return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})


@celery.task()
def create_contact():
    print('run')
    username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    first_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    last_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    contact = Contact(username=username, first_name=first_name, last_name=last_name)
    db.session.add(contact)
    db.session.commit()


@celery.task()
def remove_contact():
    time_threshold = datetime.now() - timedelta(seconds=60)
    contacts_old = Contact.query.filter(Contact.creation_time <= time_threshold)
    for c in contacts_old:
        db.session.delete(c)
    db.session.commit()

