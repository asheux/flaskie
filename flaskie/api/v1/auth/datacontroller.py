import re
from datetime import datetime, timedelta
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt
)
import pprint
from flaskie import settings
from flask import request, jsonify
from ..models import User, MainModel, BlackListToken
from flaskie.database import db, blacklistdb
from .serializers import Pagination
from .errors import user_is_valid, check_valid_email

class UserStore:
    
    def __init__(self):
        self.counter = 1
    
    def create_user(self, data):
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
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
            user = User(name, username, email, password)
            you_id = username + '00%d' % self.counter
            db[you_id] = user.toJSON()
            self.counter += 1
            access_token = create_access_token(username)
            refresh_token = create_refresh_token(username)
            response = {
                'status': 'success',
                'message': 'Successfully registered',
                'your ID': self.get_the_user_id(),
                'Authorization': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
            return response, 201


    def get_user(self, user_id):
        data = self.get_all_users()
        return data[user_id]
    
    def get_the_user_id(self):
        return list(db.keys())[-1]

    def get_all_users(self):
        return db

    def get_by_field(self, key, value):
        if self.get_all_users() is None:
            return {}
        for item in self.get_all_users().values():
            if item[key] == value:
                return item
    
    def is_admin(self):
        """
        To check if the user is an administrator
        :return:
        """
        return True
                
    def update_user(self, user_id, data):
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        user = User(name, username, email, password)
        db[user_id] = user.toJSON()

        response = {
            'status': 'user updated successfully',
            'data': user.toJSON()
        }
        return response, 200

    def delete(self, user_id):
        del db[user_id]

    def save_token(self, token):
        blacklist_token = BlackListToken(jti=token)
        try:
            # insert the token in database
            blacklistdb[self.counter] = blacklist_token.toJSON()
            pprint.pprint(blacklistdb)
            self.counter += 1
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not save'.format(e)
            }
            return response, 500