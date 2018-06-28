from flask_bcrypt import Bcrypt
from flask import json
from datetime import datetime

flask_bcrypt = Bcrypt()

class MainModel:
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else o.__dict__,
                          sort_keys=True, indent=4))

class User(MainModel):
    
    def __init__(self, name, username, email, password, admin=False, registered_on=datetime.now().isoformat(), *args):
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
    