import json
import falcon
from models import Contact, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test_app.db')
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


class ContactList(object):

    def on_get(self, req, resp):
        """In this place we need to get data from SQLAlchemy"""
        contacts = session.query(Contact).all()
        contacts = [contact.as_dict() for contact in contacts]
        # Create a JSON representation of the resource
        resp.body = json.dumps(contacts, ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200
