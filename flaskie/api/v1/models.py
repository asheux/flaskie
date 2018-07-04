from flask_bcrypt import Bcrypt
from flask import json
from datetime import datetime
from flaskie.database import blacklistdb

flask_bcrypt = Bcrypt()

class MainModel:
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else o.__dict__,
                          sort_keys=True, indent=4))

class User(MainModel):
    
    def __init__(self, name, username, email, password, admin=False, registered_on=datetime.now().isoformat()):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = registered_on
        self.admin = admin

    def set_password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '<User %r>' % self.username

class Admin(User):
    pass


class BlackListToken(MainModel):
    def __init__(self, token, blacklisted_on=datetime.now().isoformat()):
        self.token = token
        self.blacklisted_on = blacklisted_on

    def __repr__(self):
        return '<BlackListToken: {}'.format(self.token)

    def get_by_field(self, key, value):
        if blacklistdb is None:
            return {}
        for item in self.get_all_users().values():
            if item[key] == value:
                return item

    @staticmethod
    def check_blacklist(auth_token):
        """Check if the token is blacklisted"""
        res = self.get_by_field(key='token', value=str(auth_token))
        if res:
            return True
        else:
            return False