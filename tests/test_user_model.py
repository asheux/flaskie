import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    fullname = 'brian mboya'
    username = 'asheuh'
    email = 'asheuh@gmail.com'
    password = 'testing'
    role = 'user'
    obj = User(fullname, username, email, password, role)

    def test_password_setter(self):
        self.assertTrue(self.obj.password_hash is  not None)
    
    def test_password_verification(self):
        self.assertTrue(self.obj.verify_password('testing'))
        self.assertFalse(self.obj.verify_password('fuckoff'))

    def test_password_salts_are_random(self):
        obj2 = User(self.fullname, self.username, self.email, self.password, self.role)
        self.assertTrue(self.obj.password_hash != obj2.password_hash)