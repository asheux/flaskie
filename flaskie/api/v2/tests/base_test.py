import json
from unittest import TestCase
from migrate import Migration
from flaskie import create_app, settings
from flaskie.api.v1.models import User


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.migrate = Migration()
        self.migrate.set_up()
        self.client = self.app.test_client()

        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"
