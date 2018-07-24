from functools import wraps
from flask import request, json
from flask_jwt_extended import get_jwt_identity
from ..models import User

def admin_auth(f):
    """Creates the admin guard decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.get_by_field(field='id', value=get_jwt_identity())
        if not user:
            return None
        if not user['admin'] == User.is_admin():
            response_obj = {
                'status': 'fail',
                'message': 'Sorry, only an admin can perform this action'
            }
            return response_obj, 401
        return f(*args, **kwargs)
    return decorated
    