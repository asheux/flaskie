import json
from flaskie.api.v1.models import User, Requests
from .base_test import BaseTestCase

class TestAdminManageUser(BaseTestCase):
    def test_get_all_users_when_none(self):
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
                '/api/v1/admin/requests',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'There are no requests in the database yet')
            self.assertEqual(response.status_code, 404)