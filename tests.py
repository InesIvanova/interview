import os
import unittest

import requests
from flask import jsonify
from app import app, db
from models import Contact, Email
from sqlalchemy.exc import SQLAlchemyError

TEST_DB = 'test.db'

basedir = os.path.abspath(os.path.dirname(__file__))

CONNECTION_STR = 'sqlite:///' + os.path.join(basedir, TEST_DB)
MAIN_URL = 'http://127.0.0.1:5000/contacts'

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STR

        self.app = app.test_client()
        db.drop_all()
        db.create_all()



    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = requests.get(MAIN_URL)
        assert response.status_code == 200

    def test_incorrect_main_page(self):
        response = requests.get(MAIN_URL+'/')
        assert response.status_code == 404

    def test_valid_contact_registration(self):
        with app.app_context():
            response = requests.post(MAIN_URL, json={'username': 'create', 'first_name': 'contact', 'last_name': 'new'})
            assert response.status_code == 200

    def new_contact(self):
        contact = Contact(username='testContact', first_name='Test', last_name='Testov')
        return contact


if __name__ == "__main__":
    unittest.main()