from flask_restful import Resource, reqparse, request
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from models import Contact
from app import db
from flask_api import status, exceptions
import json

parser = reqparse.RequestParser()


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
        if request.form:
            data = request.form
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
            data = request.form
            contact.username = data['username']
            contact.first_name = data['first_name']
            contact.last_name = data['last_name']
            db.session.commit()
            return jsonify({'message': 'Resource Updated Successfully', 'status': status.HTTP_200_OK})
        return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})

    def delete(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({'message': 'No Content', 'status': status.HTTP_204_NO_CONTENT})
        return jsonify({'message': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})



