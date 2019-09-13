from flask_restful import Api
from app import app
from views import ContactListCreateView, ContactRetrieveUpdateDeleteView, EmailListCreateView

api = Api(app)
api.add_resource(ContactListCreateView, '/contacts')
api.add_resource(ContactRetrieveUpdateDeleteView, '/contacts/<id>')
api.add_resource(EmailListCreateView, '/emails')