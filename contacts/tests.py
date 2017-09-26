import json
import pytest

from falcon import testing
from models import Contact
from contacts.app import api


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
        "id": 1,
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    }

    contact_obj = Contact(**doc)

    assert doc == contact_obj.as_dict()


@pytest.fixture()
def client():
    return testing.TestClient(api)


def test_create_contact(client):
    body = json.dumps({
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "email": "eqwq@ewq.re",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    })

    doc = {'status': '201 Created'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_post('/contacts/', body=body, headers=headers)
    assert result.json == doc


def test_contact_list(client):
    doc = [{
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "email": "eqwq@ewq.re",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "id": 1,
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    }]

    result = client.simulate_get('/contacts/list')
    assert result.json == doc


def test_get_contact(client):
    doc = {
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "email": "eqwq@ewq.re",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "id": 1,
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    }

    result = client.simulate_get('/contacts/1')
    assert result.json == doc


def test_update_contact(client):
    body = json.dumps({
        "phone_number": 2223322,
        "city": "Sacramento",
        "first_name": "Bob",
        "last_name": "Smith",
    })
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_put('/contacts/1', body=body, headers=headers)
    assert result.json == doc


def test_delete_contact(client):
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_delete('/contacts/1', headers=headers)
    assert result.json == doc


def test_404(client):
    doc = {'status': 'Object does not exist or id is incorrect'}
    headers = {"Content-Type": "application/json"}
    result1 = client.simulate_delete('/contacts/', body=json.dumps({}), headers=headers)
    result2 = client.simulate_put('/contacts/fbfdzx', body=json.dumps({}), headers=headers)
    result3 = client.simulate_get('/contacts/fbfdzx', body=json.dumps({}), headers=headers)
    assert result1.json == doc
    assert result2.json == doc
    assert result3.json == doc


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
    result1 = client.simulate_post('/contacts/', body=body1, headers=headers)
    result2 = client.simulate_put('/contacts/', body=body2, headers=headers)
    assert result1.json == doc1
    assert result2.json == doc2


def test_incorrect_content_type(client):
    body = json.dumps({
        "phone_number": 1234,
        "city": "Berlin",
        "first_name": "Patrick",
        "last_name": "Jane",
        "country": "USA",
        "company": "dsadsadas",
        "email": "eqwq@ewq.re",
        "state": "NewYork",
        "notes": "adssadasdasd",
        "address": "eqweqweqw",
        "unit_number": "213421",
        "street_address": "zdgkrs",
        "zip_code": "11212142"
    })

    doc = {'description': 'application/x-www-form-urlencoded is an unsupported media type.',
           'title': 'Unsupported media type'}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = client.simulate_post('/contacts/', body=body, headers=headers)
    assert result.json == doc
