import json
from flaskie.api.v1.models import User
from .base_test import BaseTestCase


class TestUserLogin(BaseTestCase):
    def test_login(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully logged in as Paulla Mboya')
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(response.status_code, 201)

    def test_login_with_none_existing_username(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chessi',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'The username you provided does not exist')
            self.assertEqual(response.status_code, 404)

    def test_login_with_a_wrong_password(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='chessi'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'The password you provided (chessi) did not match the database password')
            self.assertEqual(response.status_code, 401)