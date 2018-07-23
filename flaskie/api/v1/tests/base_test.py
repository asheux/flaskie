from unittest import TestCase
from flaskie import create_app
from flaskie import settings

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.migrate = Migration()
        self.migrate.set_up()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()