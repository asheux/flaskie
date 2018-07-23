import unittest
from flask import Flask
from flask import current_app
from flaskie import create_app
from flaskie import settings

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        """Creates an environment for the test that is close to the app running"""
        self.app = create_app(settings.TESTING)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config)