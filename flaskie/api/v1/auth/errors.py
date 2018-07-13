import re
from flaskie.database import db, requestsdb
from flaskie.api.restplus import api

def user_is_valid(data):
    """user error handling"""
    from .collections import store

    errors = {}
    if store.get_by_field(key='email', value=data.get('email')) is not None:
        errors['email'] = "The email you provided is in use by another user"
    if store.get_by_field(key='username', value=data.get('username')) is not None:
        errors['username'] = "The username you provided already exists"
        
    return errors

def request_is_valid(data):
    from .collections import reqstore

    errors = {}
    if reqstore.get_by_field(key='requestname', value=data.get('requestname')) is not None:
        errors['requestname'] = "Request with the name has be created already, you might want to modify it"
    
    return errors

def abort_if_doesnt_exists(user_id):
    """Checks if given id exists in the database"""
    if user_id not in db:
        api.abort(404, "User with id {} doesn't exist or your provided an id that does not belong to you".format(user_id))
    
def abort_if_request_doesnt_exists(request_id):
    """Checks if given id exists in the database"""
    if request_id not in requestsdb:
        api.abort(404, "Request with id {} doesn't exist or your provided an id that does not belong to you".format(request_id))

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)

def not_logged_in(user):
    """Checks if user is logged in or not"""
    response_obj = {
        'status': 'fail',
        'message': 'No current user, Please log in first'
    }
    return response_obj