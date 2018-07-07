from functools import wraps
from flask import request, json
from flask_jwt_extended import get_jwt_identity
from .authAPI import Auth
from .collections import store

def admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(get_jwt_identity())
        user = data.get('data')
        if not user:
            return data, status
        if not user['admin'] == store.is_admin():
            response_obj = {
                'status': 'fail',
                'message': 'Sorry, only an admin can perform this action'
            }
            return response_obj, 401
        return f(*args, **kwargs)
    return decorated
    