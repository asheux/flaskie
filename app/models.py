from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from flask import json
from datetime import datetime

class MainModel:
    def to_json(self, exclude=True):
        """Converts the response to json object"""
        return json.loads(self.json_str(exclude))

    def json_str(self, exclude=True):
        """Converts to json string object"""
        pass
class User(MainModel):
    
    def __init__(self, fullname, username, email, password,role, registered_on=datetime.now()):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = registered_on
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Admin(User):
    pass
