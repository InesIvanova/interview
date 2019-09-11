from flask_restful import Resource, reqparse, request
from flask import jsonify, request
from models import Contact
from app import db
import json

parser = reqparse.RequestParser()


class ContactListCreateView(Resource):
    def get(self):
        if request.args:
            username = request.args.to_dict()['username']
            contact = Contact.query.filter_by(username=username).first()
            if contact:
                return jsonify(contact.serialize)
            return jsonify({'error': 'no such username'})
        contacts = Contact.query.all()
        return jsonify({'contacts': [result.serialize for result in contacts]})

    def post(self):
        if request.form:
            #TODO get the data in specific format from form and
            # replace in contact and include error handling
            data = request.form
            contact = Contact(username='noraa2', first_name='Nora', last_name='Kenova')
            db.session.add(contact)
            db.session.commit()
            return jsonify({'status': '201'})
        else:
            print('noo')
            return jsonify({'error': 'error'})


class ContactRetrieveUpdateDeleteView(Resource):
    def get(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            return jsonify(contact.serialize)
        return jsonify({'error': 'no such id'})

    def update(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            #TODO get this from form (as in post request) replace value and save it to db
            db.session.update()
            return jsonify(contact.serialize)
        return jsonify({'error': 'no such id'})

    def delete(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({'delete': 'ok'})
        return jsonify({'error': 'no such id'})


