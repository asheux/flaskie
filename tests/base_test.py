from unittest import TestCase
from run import create_app
from flaskie import settings

class BaseTestCase(TestCase):
    api_prefix = "/api/v1/"

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def full_endpoint(self, path=""):
        return self.api_prefix + path
    
    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()