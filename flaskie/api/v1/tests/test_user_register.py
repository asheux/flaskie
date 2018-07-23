import json
from flaskie.api.v1.models import User
from .base_test import BaseTestCase

class TestUserRegister(BaseTestCase):

    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register', 
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully registered')
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(response.status_code, 201)
    
    def test_registration_with_invalid_email(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register', 
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuhgmail.com',
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'error')
            self.assertTrue(response_data['message'] == 'Not a valid email address, please try again')
            self.assertEqual(response.status_code, 403)
        
    def test_registration_if_user_exits(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register', 
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='paulla@gmail.com',
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            errors = {
                "username": "The username you provided already exists",
                "email": "The email you provided is in use by another user"
            }
            self.assertTrue(response_data['status'] == 'error')
            self.assertTrue(response_data['message'] == errors)
            self.assertEqual(response.status_code, 401)