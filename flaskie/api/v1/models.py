from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from flask import json
from datetime import datetime

class MainModel:
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else o.__dict__,
                          sort_keys=True, indent=4))

class User(MainModel):
    
    def __init__(self, name, username, email, password, role, registered_on=datetime.utcnow().isoformat()):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = registered_on
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Admin(User):
    pass
    