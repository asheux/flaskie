import re
from flask import request, jsonify
from ..models import User, MainModel
from flaskie.database import db
from .serializers import Pagination
from .errors import user_is_valid, check_valid_email

class UserStore:
    
    def __init__(self):
        self.counter = 1
    
    def create_user(self, data):
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password_hash']
        role = data['role']
        errors = user_is_valid(data)

        if check_valid_email(email) is None:
            response = {
                'status': 'error',
                'message': 'Not a valid email address, please try again'
            }
            return response, 403
        
        elif errors:
            response = {
                'status': 'error',
                'message': errors
            }
            return response
        else:
            user = User(name, username, email, password, role)
            
            db[self.counter] = user.toJSON()
            self.counter += 1

            response = {
                'status': 'success',
                'message': 'Successfully registered',
                'new_user': user.toJSON()
            }
            return response, 201


    def get_user(self, user_id):
        data = self.get_all_users()
        return data[user_id]
        

    def get_all_users(self):
        return db

    def get_by_field(self, key, value):
        if self.get_all_users() is None:
            return []
        for item in self.get_all_users().values():
            if item[key] == value:
                return item
                
    def update_user(self, user_id, data):
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password_hash']
        role = data['role']
        user = User(name, username, email, password, role)
        db[user_id] = user.toJSON()

        response = {
            'status': 'user updated successfully',
            'data': user.toJSON()
        }
        return response, 200

    def delete(self, user_id):
        del db[user_id]