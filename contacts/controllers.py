import json
import falcon

from marshmallow import ValidationError

from .models import Contact
from .serializers import ContactSerializer
from make_engine import DBSession


class BaseContactController(object):
    """
    General implementations for contact classes
    """

    serializer = ContactSerializer(strict=True)

    @staticmethod
    def response_404(resp):
        resp.body = json.dumps({
            "status": "Object does not "
                      "exist or id is incorrect"
        })
        resp.status = falcon.HTTP_404

    @staticmethod
    def response_400(resp, err):
        resp.body = json.dumps(err.messages)
        resp.status = falcon.HTTP_400

    @staticmethod
    def get_contact(session, contact_id):
        if contact_id:
            return session.query(Contact).get(contact_id)


class ContactCRUD(BaseContactController):
    """
    Allows:
        Create contact on POST
        Retrieve detail info about contact on GET
        Update contact info on PUT
        Delete contact info on DELETE
    Returns data in JSON format.
    """

    def on_get(self, req, resp, contact_id=None):
        session = DBSession()
        contact = self.get_contact(session, contact_id)

        if contact:
            contact = contact.as_dict()
        else:
            return self.response_404(resp)

        resp.body = json.dumps(contact, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):

        session = DBSession()
        data = req.media

        try:
            serialized = self.serializer.load(data=data)
        except ValidationError as err:
            return self.response_400(resp, err)

        contact = serialized.data
        session.add(contact)
        session.commit()
        resp.body = json.dumps(contact.as_dict())
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, contact_id=None):

        session = DBSession()
        data = req.media

        try:
            serialized = self.serializer.load(data=data, partial=True)
        except ValidationError as err:
            return self.response_400(resp, err)

        serialized_data = serialized.data.as_dict()
        contact = self.get_contact(session, contact_id)

        if contact:
            for name, value in serialized_data.items():
                if value:
                    setattr(contact, name, value)
        else:
            return self.response_404(resp)

        session.commit()

        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, contact_id=None):
        session = DBSession()
        contact = self.get_contact(session, contact_id)

        if contact:
            session.delete(contact)
            session.commit()
        else:
            return self.response_404(resp)

        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200


class ContactList(BaseContactController):
    """
    Controller for list displaying all contacts on GET
    """

    def on_get(self, req, resp):
        session = DBSession(autocommit=True)

        contacts = session.query(Contact).all()
        contacts = [contact.as_dict() for contact in contacts]

        resp.body = json.dumps(contacts, ensure_ascii=False)
        resp.status = falcon.HTTP_200
