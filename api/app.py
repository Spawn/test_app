import falcon

from contacts import ContactList, \
    ContactDetail, \
    ContactCreate, \
    ContactUpdate,\
    ContactDelete

api = application = falcon.API()

contacts_list = ContactList()
contact_detail = ContactDetail()
contact_create = ContactCreate()
contact_update = ContactUpdate()
contact_delete = ContactDelete()

api.add_route('/contacts', contacts_list)
api.add_route('/contacts/{contact_id}/', contact_detail)
api.add_route('/contacts/create/', contact_create)
api.add_route('/contacts/update/{contact_id}/', contact_update)
api.add_route('/contacts/delete/{contact_id}/', contact_delete)
