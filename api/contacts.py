import json
import falcon
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from marshmallow import ValidationError

from models import Contact, Base
from api.serializers import ContactSerializer

engine = create_engine(settings.SQLITE_ENGINE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


class ContactCreate(object):
    serializer = ContactSerializer(strict=True)

    def on_post(self, req, resp):

        session = DBSession()

        data = req.media

        try:
            serialized = self.serializer.load(data=data)
        except ValidationError as err:
            resp.body = json.dumps(err.messages)
            resp.status = falcon.HTTP_400
            return

        contact = serialized.data
        session.add(contact)
        session.commit()
        resp.body = json.dumps({"status": "201 Created"})
        resp.status = falcon.HTTP_201


class ContactList(object):

    def on_get(self, req, resp):
        session = DBSession(autocommit=True)

        contacts = session.query(Contact).all()
        contacts = [contact.as_dict() for contact in contacts]

        resp.body = json.dumps(contacts, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class ContactDetail(object):

    def on_get(self, req, resp, contact_id):
        session = DBSession()

        contact = session.query(Contact).get(contact_id)
        if contact:
            contact = contact.as_dict()
        else:
            resp.body = json.dumps({
                "status": "404 Object does not exist"
            })
            resp.status = falcon.HTTP_404
            return

        resp.body = json.dumps(contact, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class ContactUpdate(object):
    serializer = ContactSerializer(strict=True)

    def on_put(self, req, resp, contact_id):

        session = DBSession()

        data = req.media
        try:
            serialized = self.serializer.load(data=data, partial=True)
        except ValidationError as err:
            resp.body = json.dumps(err.messages)
            resp.status = falcon.HTTP_400
            return

        serialized_data = serialized.data.as_dict()
        contact = session.query(Contact).get(contact_id)

        if contact:
            for name, value in serialized_data.items():
                if value:
                    setattr(contact, name, value)
        else:
            resp.body = json.dumps({
                "status": "404 Object does not exist"
            })
            resp.status = falcon.HTTP_404
            return

        session.commit()
        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200


class ContactDelete(object):

    def on_delete(self, req, resp, contact_id):
        session = DBSession()
        contact = session.query(Contact).get(contact_id)

        if contact:
            session.delete(contact)
            session.commit()
        else:
            resp.body = json.dumps({
                "status": "404 Object does not exist"
            })
            resp.status = falcon.HTTP_404
            return

        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200
