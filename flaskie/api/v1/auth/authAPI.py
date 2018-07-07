from flask_bcrypt import Bcrypt
from flask import request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt
)
from .collections import store
from .errors import not_logged_in

flask_bcrypt = Bcrypt()

class Auth:
    @staticmethod
    def login_user(data):
        try:
            data = request.json
            user = store.get_by_field(key='username', value=data.get('username'))
            if not user:
                response = {
                    'status': 'fail',
                    'message': 'The username you provided does not exist'
                }
                return response, 404
            elif not flask_bcrypt.check_password_hash(user['password_hash'], data.get('password')):
                response = {
                    'status': 'fail',
                    'message': 'The password you provided ({}) did not match the database password'.format(data.get('password'))
                }
                return response, 401
            else:
                access_token = create_access_token(user['username'])
                refresh_token = create_refresh_token(user['username'])
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in as {}'.format(user['name']),
                    'Authorization': {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }
                return response, 201

        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not login: {}, try again.'.format(e)
            }
            return response, 500

    @staticmethod
    def logout_user(data):
        return store.save_token(data)


    @staticmethod
    def get_logged_in_user(identity):
        # get the auth token
        user = store.get_by_field(key='username', value=identity)
        if user is not None:
            response_obj = {
                'status': 'success',
                'data': {
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'admin': user['admin'],
                    'password': user['password_hash'],
                    'registered_on': user['registered_on']
                }
            }
            return response_obj, 200
        else:
            response_obj = {
                'status': 'fail',
                'message': 'user is none'
            }
            return response_obj