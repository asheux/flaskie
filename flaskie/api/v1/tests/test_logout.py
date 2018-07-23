import json
from .base_test import BaseTestCase

class TestLogout(BaseTestCase):
    def test_logout(self):
        with self.client:
            response_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response_login.data.decode())
            print(response_login.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully logged in as Paulla Mboya')
            self.assertTrue(response_data['Authorization']['access_token'])
            self.assertEqual(response_login.status_code, 201)

            # valid logout
            response = self.client.post(
                '/api/v1/auth/logout_access',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Access token has been revoked, you are now logged out')
            self.assertEqual(response.status_code, 200)

    def test_logout_refresh(self):
        with self.client:
            response_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response_login.data.decode())
            print(response_login.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully logged in as Paulla Mboya')
            self.assertTrue(response_data['Authorization']['access_token'])
            self.assertEqual(response_login.status_code, 201)

            # valid logout
            response = self.client.post(
                '/api/v1/auth/logout_refresh',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_login.data.decode()
                    )['Authorization']['refresh_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Refresh token has been revoked')
            self.assertEqual(response.status_code, 200)

    def test_token_refresh(self):
        with self.client:
            response_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='paulla',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response_login.data.decode())
            print(response_login.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully logged in as Paulla Mboya')
            self.assertTrue(response_data['Authorization']['access_token'])
            self.assertEqual(response_login.status_code, 201)

            # valid logout
            response = self.client.post(
                '/api/v1/auth/refresh_token',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_login.data.decode()
                    )['Authorization']['refresh_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'token refreshed successfully')
            self.assertEqual(response.status_code, 201)