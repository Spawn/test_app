from marshmallow import Schema, fields, post_load

from models import Contact


class ContactSerializer(Schema):
    """
    Class for serialize and deserialize contact data
    """

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Integer()
    company = fields.String()
    address = fields.String()
    street_address = fields.String(required=True)
    unit_number = fields.String()
    city = fields.String(required=True)
    state = fields.String(required=True)
    zip_code = fields.String(required=True)
    country = fields.String()
    notes = fields.String()

    @post_load
    def make_user(self, data):
        return Contact(**data)
