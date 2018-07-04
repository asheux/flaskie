import re
from datetime import datetime, timedelta
import jwt
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

            response = {
                'status': 'success',
                'message': 'Successfully registered',
                'your ID': self.get_the_user_id(),
                'Authorization': generate_token(username)
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
        blacklist_token = BlackListToken(token=token)
        try:
            # insert the token in database
            blacklistdb[self.counter] = blacklist_token.toJSON()
            self.counter += 1

            response = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return response, 200
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not logout'.format(e)
            }
            return response, 500

def generate_token(user):
    g_token = GenerateToken()
    try:
        auth_token = g_token.encode_auth_token(user)
        return auth_token.decode()
    except Exception as e:
        response = {
            'status': 'fail',
            'message': 'Could not generate token: {}'.format(e)
        }
        return response

class GenerateToken:
    def encode_auth_token(self, username):
        """
        Generates the auth token
        :return string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': username
            }
            return jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY)
            is_blacklisted_token = BlackListToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted, please login again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, please login again'
        except jwt.InvalidTokenError:
            return 'Invalid token, please login again'