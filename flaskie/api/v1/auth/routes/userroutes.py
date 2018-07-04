import logging
from flask import request, jsonify
from flask_restplus import Resource
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user_register, page_of_users, Pagination, user_login
from ..collections import store
from ..errors import abort_if_doesnt_exists
from ..authAPI import Auth
from ..decorators import admin_token_required, token_required

log = logging.getLogger(__name__)
ns_auth = api.namespace('auth', description='Authentication operations')
ns = api.namespace('user', description='User operations')
ns_admin = api.namespace('admin', description='Admin Management')

@ns.route('/register')
class UsersCollection(Resource):
    @api.doc(pagination_arguments)
    @api.response(201, 'User created successfully')
    @api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return store.create_user(data=data)

@ns.route('/<string:user_id>')
@api.response(404, 'User with the given id not found')
class UserItem(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.response(200, 'success')
    @token_required
    @api.doc(security='apikey')
    def get(self, user_id):
        """Returns a user by a given id"""
        abort_if_doesnt_exists(user_id)
        response = {
            "data": store.get_user(user_id)
        }
        return response, 200

@ns_admin.route('/users')
class AdminManagementResource(Resource):
    '''Shows a list of all users'''
    @api.doc(security='apikey')
    @admin_token_required
    @api.expect(pagination_arguments)
    def get(self):
        """Return list of users"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        users_query = store.get_all_users()
        paginate = Pagination(page, per_page, len(users_query))
        # result = {k:v for k, v in [(k,v) for item in users_query for k, v in item.items()]}
        if users_query == {}:
            response = {
                "message": "There are no users in the database yet"
            }
            return response, 404
        else:
            response = {
                "page": paginate.page,
                "per_page": paginate.per_page,
                "total": paginate.total_count,
                "data": users_query
            }
            return response, 200

@ns_admin.route('/users/<string:user_id>')
class AdminManagementItem(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.response(200, 'success')
    @api.doc(security='apikey')
    @admin_token_required
    def get(self, user_id):
        """Returns a user by a given id"""
        abort_if_doesnt_exists(user_id)
        response = {
            "data": store.get_user(user_id)
        }
        return response, 200

    '''@api.doc(pagination_arguments)
    @api.response(200, 'User updated successfully')
    @api.expect(user, validate=True)
    def put(self, user_id):
        """Updates user details"""
        abort_if_doesnt_exists(user_id)
        data = request.json
        return store.update_user(user_id, data)'''

    @api.doc(security='apikey')
    @admin_token_required
    @api.response(204, 'User deleted')
    def delete(self, user_id):
        """Deletes a user with the given id"""
        abort_if_doesnt_exists(user_id)
        store.delete(user_id)
        response = {
            'status': 'success',
            'message': 'user with id {} deleted successfully'.format(user_id)
        }
        return response, 200

@ns_auth.route('/login')
class UserLoginResource(Resource):
    @api.doc('login user')
    @api.response(201, 'Login successful')
    @api.expect(user_login, validate=True)
    def post(self):
        data = request.json
        return Auth.login_user(data=data)

@ns_auth.route('/logout')
class UserLogoutResource(Resource):
    @api.doc(security='apikey')
    @api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)