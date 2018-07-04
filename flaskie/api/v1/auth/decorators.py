from functools import wraps
from flask import request
from .authAPI import Auth

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')
        if not token:
            return data, status
        return f(*args, **kwargs)
    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
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

    return decorated