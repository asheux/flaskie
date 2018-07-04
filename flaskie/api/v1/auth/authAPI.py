from flask_bcrypt import Bcrypt
from flask import request
from .collections import store, g_token

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
                    'message': 'The password you provided ({}) did not match the database password'.format(password)
                }
                return response, 401
            else:
                auth_token = g_token.encode_auth_token(user['username'])
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in as {}'.format(user['name']),
                        'Authorization': auth_token.decode()
                    }
                    return response, 200

        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not login: {}, try again.'.format(e)
            }
            return response, 500

    @staticmethod
    def logout_user(data):
        if data:
            try:
                auth_token = data.split(" ")[1]
            except IndexError as e:
                response_obj = {
                    'status': 'fail',
                    'message': 'Bearer token malformed: {}'.format(e)
                }
                return response_obj, 401
        else:
            auth_token = ''
        if auth_token:
            resp = g_token.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # then mark the token as blacklisted
                return store.save_token(token=auth_token)
            else:
                response = {
                    'status': 'fail',
                    'message': resp
                }
                return response, 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a token'
            }
            return response, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_header = new_request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_obj = {
                    'status': 'fail',
                    'message': 'Bearer token malformed'
                }
                return response_obj, 401
        else:
            auth_token = ''
        if auth_token:
            response = g_token.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user = store.get_by_field(key='username', value=response)
                response_obj = {
                    'status': 'success',
                    'data': {
                        'name': user['name'],
                        'username': user['username'],
                        'email': user['email'],
                        'admin': user['admin'],
                        'registered_on': user['registered_on']
                    }
                }
                return response_obj, 200
            response_obj = {
                'status': 'fail',
                'message': response
            }
            return response_obj, 401
        else:
            response_obj = {
                'status': 'fail',
                'message': 'provide a token to access this route'
            }
            return response_obj, 401