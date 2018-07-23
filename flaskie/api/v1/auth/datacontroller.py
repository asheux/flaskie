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
from flaskie.database import get_current_user
from ..models import User, MainModel, BlackListToken, Requests
from flaskie.database import db, blacklistdb, requestsdb
from .serializers import Pagination
from .errors import user_is_valid, check_valid_email

class UserStore:
    """The class controls the adding and fetching a user in the database"""
    
    def __init__(self):
        """Initializes the counter id"""
        self.counter = 1
    
    def create_user(self, data):
        """Creates a new user and adds the user in the database"""
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
            return response, 401
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
        """Gets a single user in the database by a given id"""
        data = self.get_all_users()
        return data[user_id]
    
    def get_the_user_id(self):
        """Gets the last added user's id from the database"""
        return list(db.keys())[-1]

    def get_all_users(self):
        """Gets all the available users from the database"""
        return db

    def get_by_field(self, key, value):
        """Gets a user by a given field"""
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
        """Updates or modifies a given user by id"""
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        user = User(name, username, email, password)
        db[user_id] = user.toJSON()

        response = {
            'status': 'success',
            'message': 'user updated successfully',
            'data': user.toJSON()
        }
        return response, 200

    def save_token(self, token):
        """Saves the blacklisted token in the database"""
        blacklist_token = BlackListToken(jti=token)
        try:
            # insert the token in database
            blacklistdb[self.counter] = blacklist_token.toJSON()
            self.counter += 1
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not save'.format(e)
            }
            return response, 500

class RequestStore:
    def __init__(self):
        self.index = 1

    def create_request(self, data):
        requestname = data['requestname']
        description = data['description']
        requests = Requests(requestname, description, created_by=get_current_user())
        requestsdb[self.index] = requests.toJSON()
        self.index += 1

        response = {
            'status': 'success',
            'message': 'requests created successfully',
            'data': requests.toJSON()
        }
        return response, 201

    def get_all_requests(self):
        """Gets all requests in the database"""
        return requestsdb

    def get_by_field(self, key, value):
        """Gets a request by a given field"""
        if self.get_all_requests() is None:
            return {}
        for item in self.get_all_requests().values():
            if item[key] == value:
                return item

    def get_one_request(self, request_id):
        """Gets a single request by a given request id"""
        data = self.get_all_requests()
        return data[request_id]