from .controllers import ContactList, ContactCRUD
import falcon

api = application = falcon.API()

contacts_list = ContactList()
contact_crud = ContactCRUD()

api.add_route('/contacts', contact_crud)
api.add_route('/contacts/{contact_id}', contact_crud)
api.add_route('/contacts/list/', contacts_list)
