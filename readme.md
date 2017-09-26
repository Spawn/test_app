# Test API app

Test REST API for contacts management.

## Installation

Clone project from repo:
`git clone http://github.com/spawn/test_app`

Move to project directory:
`cd test_app`

Install environment with 2.7 or 3+ python version:
`virtualenv .env`

Activate environment:
`. .env/bin/activate`

Install requirements:
`pip install -r requirements`

Setup database:

`export PYTHONPATH=$PWD:$PYTHONPATH`

`python contacts/models.py`

## Run tests

_Note: before test running specify path for test database in pytest.ini_

`pytest contacts/tests.py -v`

## Usage

Run server:
`gunicorn --reload contacts.app`

Available endpoints:

'/contacts' - Allows POST method for contact creating

'/contacts/{contact_id}' - Allows:

    GET - detail contact information 
    PUT - update contact object
    DELETE - delete contact object

'/contacts/list/' - Allows GET for getting contacts list

All endpoints returns JSON data type.

Accepted Content-Type - application/json
