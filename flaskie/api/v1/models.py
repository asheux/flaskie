from flask_bcrypt import Bcrypt
from flask import json
from datetime import datetime
from flaskie.database import blacklistdb

flask_bcrypt = Bcrypt()

def get_by_field(key, value):
    if blacklistdb is None:
        return {}
    for item in blacklistdb.values():
        if item[key] == value:
            return item

class MainModel:
    """This is the base model that creates common functions"""
    def toJSON(self):
        """Converts json string object to a dictionary"""
        return json.loads(json.dumps(self, default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else o.__dict__,
                          sort_keys=True, indent=4))

class User(MainModel):
    """Creates the user model"""
    def __init__(self, 
        name, username, email, 
        password, admin=False, 
        registered_on=datetime.now().isoformat()):
        """Initializes the user model"""

        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = registered_on
        self.admin = admin

    def set_password(self, password):
        """Sets the hashed password"""
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify that the hashed password matches the user input password"""
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Represents the user by the user's username"""
        return '<User %r>' % self.username

class BlackListToken(MainModel):
    """Creates the blacklisting model"""
    def __init__(self, jti, blacklisted_on=datetime.now().isoformat()):
        """Initializes the blacklist model"""
        self.jti = jti
        self.blacklisted_on = blacklisted_on

    def __repr__(self):
        return '<BlackListToken: {}'.format(self.jti)

    @classmethod
    def check_blacklist(cls, auth_token):
        """Check if the token is blacklisted"""
        res = get_by_field(key='jti', value=auth_token)
        return bool(res)


class Requests(MainModel):
    def __init__(self, 
        requestname, 
        description,
        created_by=None, 
        date_created=datetime.now(), 
        date_modified=datetime.now()):

        self.requestname = requestname
        self.description = description
        self.created_by = created_by
        self.date_created = date_created
        self.date_modified = date_modified

    def __repr__(self):
        return '<Requests %r>' % self.requestname