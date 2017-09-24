import falcon

from contacts import ContactList


api = application = falcon.API()

contacts = ContactList()

api.add_route('/contacts', contacts)
