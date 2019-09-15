from app import app, db
from models import Contact

import os
import unittest
import requests

TEST_DB = 'test.db'

basedir = os.path.abspath(os.path.dirname(__file__))

CONNECTION_STR = 'sqlite:///' + os.path.join(basedir, TEST_DB)
MAIN_URL = 'http://127.0.0.1:5000/contacts'

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STR

        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass


    # helpers

    def new_contact(self):
        contact = Contact(username='testContact', first_name='Test', last_name='Testov')
        db.session.add(contact)
        db.session.commit()

    def generate_username(self):
        import random
        import string
        letters = string.ascii_lowercase
        username = ''.join(random.choice(letters) for i in range(40))
        return username


    # tests

    def test_main_page(self):
        response = requests.get(MAIN_URL)
        assert response.status_code == 200

    def test_incorrect_main_page(self):
        response = requests.get(MAIN_URL+'/')
        assert response.status_code == 404

    def test_valid_contact_registration(self):
        with app.app_context():
            username = self.generate_username()
            response = requests.post(MAIN_URL, json={'username': username, 'first_name': 'contact', 'last_name': 'new'})
            assert response.status_code == 200

    def test_put_contact(self):
        with app.app_context():
            username = self.generate_username()
            response = requests.put(MAIN_URL+'/3', json={'username': username, 'first_name': 'contact', 'last_name': 'new'})
            assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()