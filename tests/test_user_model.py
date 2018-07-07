import unittest
from flaskie.api.v1.models import User

class UserModelTestCase(unittest.TestCase):
    name = 'brian mboya'
    username = 'asheuh'
    email = 'asheuh@gmail.com'
    password = 'testing'
    admin = False
    obj = User(name, username, email, password, admin)

    def test_password_setter(self):
        self.assertTrue(self.obj.password_hash is not None)
    
    def test_password_verification(self):
        self.assertTrue(self.obj.verify_password('testing'))
        self.assertFalse(self.obj.verify_password('fuckoff'))

    def test_password_salts_are_random(self):
        obj2 = User(self.name, self.username, self.email, self.password, self.admin)
        self.assertTrue(self.obj.password_hash != obj2.password_hash)