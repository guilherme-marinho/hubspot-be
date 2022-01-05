from flask import Flask, Response, request
from flask_cors import CORS
from hubspot import HubSpot
from hubspot.auth.oauth import *
import json

from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/create_contact', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        api_key = request.headers.get('Authorization')
        api_client = HubSpot(api_key=api_key)
        simple_public_object_input = SimplePublicObjectInput(
            properties={"email": data['email'],
                        "firstname": data['firstname'],
                        "lastname": data['lastname']}
        )
        api_client.crm.contacts.basic_api.create(simple_public_object_input=simple_public_object_input)
        return Response(content_type='Application/json',
                        status=201)
    except ApiException as e:
        print("Exception when requesting contact by id: %s\n" % e)


@app.route('/update_contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        data = request.get_json()
        api_key = request.headers.get('Authorization')
        api_client = HubSpot(api_key=api_key)
        simple_public_object_input = SimplePublicObjectInput(
            properties={"email": data['email'],
                        "firstname": data['firstname'],
                        "lastname": data['lastname']}
        )
        api_client.crm.contacts.basic_api.update(contact_id=contact_id,
                                                 simple_public_object_input=simple_public_object_input)
        return Response(content_type='Application/json',
                        status=204)

    except ApiException as e:
        print("Exception when requesting contact by id: %s\n" % e)


@app.route('/contact/<int:contact_id>')
def get_contact_by_id(contact_id):
    try:
        api_key = request.headers.get('Authorization')
        api_client = HubSpot(api_key=api_key)
        api_client.crm.contacts.basic_api.get_by_id(contact_id)
        contact_fetched = api_client.crm.contacts.basic_api.get_by_id(contact_id).to_dict()

        return json.dumps(contact_fetched, indent=4, sort_keys=True, default=str)
    except ApiException as e:
        print("Exception when requesting contact by id: %s\n" % e)


@app.route('/get_all', methods=['GET'])
def get_all_contact():
    try:
        api_key = request.headers.get('Authorization')
        api_client = HubSpot(api_key=api_key)
        all_contacts = transform_to_dict(api_client.crm.contacts.get_all())

        return json.dumps(all_contacts, indent=4, sort_keys=True, default=str)
    except ApiException as e:
        print("Exception when calling create_token method: %s\n" % e)


def transform_to_dict(all_contacts):
    for i in range(len(all_contacts)):
        all_contacts[i] = all_contacts[i].to_dict()
    return all_contacts


if __name__ == "__main__":
    app.run()
