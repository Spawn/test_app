import json
import pytest

from falcon import testing
from models import *
from contacts.app import api
from sqlalchemy.orm import sessionmaker


def setup_module(module):
    engine = create_engine(settings.SQLITE_DB_PATH)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


@pytest.fixture
def contact_data():
    return {
        u"phone_number": 1241212412,
        u"city": u"NewYork",
        u"first_name": u"Bob",
        u"last_name": u"qew",
        u"country": u"USA",
        u"company": u"dsadsadas",
        u"email": u"eqwq@ewq.re",
        u"state": u"NewYork",
        u"notes": u"adssadasdasd",
        u"address": u"eqweqweqw",
        u"unit_number": u"213421",
        u"street_address": u"zdgkrs",
        u"zip_code": u"11212142"
    }


@pytest.fixture
def session(request):
    engine = create_engine(settings.SQLITE_DB_PATH)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


@pytest.fixture
def contact_instance(request, contact_data, session):
    contact_obj = Contact(**contact_data)

    def fin():
        _cleanup_contact(session)

    session.add(contact_obj)
    session.commit()

    request.addfinalizer(fin)

    return contact_obj


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_model_to_dict():
    doc = {
        "phone_number": 1241212412,
        "city": "NewYork",
        "first_name": "Bob",
        "last_name": "qew",
        "country": "USA",
        "company": "dsadsadas",
        "email": "eqwq@ewq.re",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "id": None,
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    }

    contact_obj = Contact(**doc)

    assert doc == contact_obj.as_dict()


def _cleanup_contact(session):
    session.query(Contact).delete()
    session.commit()


def test_create_contact(client, session):
    contact_dict = contact_data()
    body = json.dumps(contact_dict)

    doc = contact_dict

    headers = {"Content-Type": "application/json"}
    result = client.simulate_post(
        '/contacts/', body=body, headers=headers
    ).json
    result.pop('id')
    assert result == doc

    _cleanup_contact(session)


def test_contact_list(client, contact_instance, contact_data):
    doc = [contact_instance.as_dict()]

    result = client.simulate_get('/contacts/list')
    assert result.json == doc, 'Contacts list has been not founded'


def test_get_contact(client, contact_instance, contact_data):
    doc = contact_instance.as_dict()

    result = client.simulate_get(
        '/contacts/%s' % contact_instance.id
    )
    assert result.json == doc, 'Contact has been not founded'


def test_update_contact(client, contact_instance):
    body = json.dumps({
        "phone_number": 2223322,
        "city": "Sacramento",
        "first_name": "Bob",
        "last_name": "Smith",
    })
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_put(
        '/contacts/%s' % contact_instance.id, body=body, headers=headers
    )
    assert result.json == doc, 'Contact has been not updated'


def test_delete_contact(client, contact_instance):
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_delete(
        '/contacts/%s' % contact_instance.id, headers=headers
    )
    assert result.json == doc, 'Contact has been not deleted'


def test_404(client):
    doc = {'status': 'Object does not exist or id is incorrect'}
    headers = {"Content-Type": "application/json"}

    result1 = client.simulate_delete(
        '/contacts/', body=json.dumps({}), headers=headers
    )
    result2 = client.simulate_put(
        '/contacts/-1', body=json.dumps({}), headers=headers
    )
    result3 = client.simulate_get(
        '/contacts/-1', body=json.dumps({}), headers=headers
    )

    assert result1.json == doc, 'Passed request which is not provided'
    assert result2.json == doc, 'Passed request which is not provided'
    assert result3.json == doc, 'Passed request which is not provided'


def test_400(client):
    doc1 = {'email': ['Missing data for required field.'],
            'zip_code': ['Missing data for required field.']}

    doc2 = {'email': ['Not a valid email address.']}

    body1 = json.dumps({
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "street_address": "zdgkrs",
    })

    body2 = json.dumps({
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "email": "sgasasg",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    })

    headers = {"Content-Type": "application/json"}

    result1 = client.simulate_post(
        '/contacts/', body=body1, headers=headers
    )
    result2 = client.simulate_put(
        '/contacts/', body=body2, headers=headers
    )

    assert result1.json == doc1, 'Passed object with missed required fields'
    assert result2.json == doc2, 'Passed object with wrong field format'


def test_incorrect_content_type(client, contact_data):
    body = json.dumps(contact_data)

    doc = {'description': 'application/x-www-form-urlencoded is an unsupported media type.',
           'title': 'Unsupported media type'}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = client.simulate_post('/contacts/', body=body, headers=headers)
    assert result.json == doc, 'Passed wrong content-type'
