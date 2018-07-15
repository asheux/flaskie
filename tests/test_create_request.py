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

    def test_user_cannot_modify_others_requests(self):
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='avril',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/api/v1/user/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    requestname='Malware',
                    description='slow internet'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'You are not permitted to view or update this request')
            self.assertEqual(response.status_code, 401)

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
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Purity Mboya',
                    email='puri@gmail.com',
                    username='puri',
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
                    username='paulla',
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

    def test_admin_can_modify_requests(self):
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            res_create = self.client.post(
                '/api/v1/user/requests',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    requestname='Internet',
                    description='slow internet'
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/api/v1/admin/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    status='Approved'
                )),
                content_type='application/json'
            )
            print(response)
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully Approved this request')
            self.assertEqual(response.status_code, 200)

    def test_admin_cannot_modify_pending_requests(self):
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/api/v1/admin/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    status='Approved'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'request could not be Approved because it is not Pending')
            self.assertEqual(response.status_code, 403)

    def test_user_can_modify_request(self):
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/api/v1/user/requests/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    requestname='Malware',
                    description='slow internet'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'request updated successfully')
            self.assertEqual(response.status_code, 200)

    def test_get_all_requests_for_a_logged_in_user(self):
        with self.client:
            resp_login = self.client.post(
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
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)