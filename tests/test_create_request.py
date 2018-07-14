import json
from flaskie.api.v1.models import User, Requests
from .base_test import BaseTestCase

class TestUserRegister(BaseTestCase):

    def test_create_requests(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Avril Mboya',
                    email='avril@gmail.com',
                    username='avril',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/user/requests',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    requestname='Internet',
                    description='slow internet'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'requests created successfully')
            self.assertEqual(response.status_code, 201)

    def test_get_requests_for_logged_in_user(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='avril',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/user/requests',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_requests_for_a_logged_in_user_is_none(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/user/requests',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'The current user has no request in the db')
            self.assertEqual(response.status_code, 404)

    def test_get_single_request_by_user(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='avril',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/user/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_get_request_that_is_not_yours(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Ble Mboya',
                    email='ble@gmail.com',
                    username='ble',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/user/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'You are no allowed to view or update this request')
            self.assertEqual(response.status_code, 401)