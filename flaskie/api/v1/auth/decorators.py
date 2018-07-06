from functools import wraps
from flask import request, json
from .authAPI import Auth

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data, status = Auth.get_logged_in_user(request)
            token = data.get('data')
            if not token:
                return data, status

            admin = token.get('admin')
            if not admin:
                response_obj = {
                    'status': 'fail',
                    'message': 'Admin is the only one required to view this'
                }
                return response_obj, 401

            return f(*args, **kwargs)
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'error: {}'.format(e)
            }
            return response

    return decorated