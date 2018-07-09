import logging
from flask import request, jsonify
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    create_access_token,
    get_raw_jwt
)
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user_register, page_of_users, Pagination, user_login
from ..collections import store
from ..errors import abort_if_doesnt_exists
from ..authAPI import Auth
from ..decorators import admin_auth

log = logging.getLogger(__name__)
ns_auth = api.namespace('auth', description='Authentication operations')
ns = api.namespace('user', description='User operations')
ns_admin = api.namespace('admin', description='Admin Management')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @api.doc(pagination_arguments)
    @api.response(201, 'User created successfully')
    @api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return store.create_user(data=data)

@ns.route('')
@api.response(404, 'User with the given id not found')
class UserItem(Resource):
    """Show a single todo item and lets you delete them"""
    @api.response(200, 'success')
    @jwt_required
    @api.doc('user gets their details')
    def get(self):
        """Returns a logged in user's details"""
        current_user = get_jwt_identity()
        return Auth.get_logged_in_user(current_user)
    

    @api.doc(pagination_arguments)
    @jwt_required
    @api.response(200, 'User updated successfully')
    @api.expect(user_register, validate=True)
    def put(self, user_id):
        """Updates user details"""
        abort_if_doesnt_exists(user_id)
        data = request.json
        return store.update_user(user_id, data)

@ns_admin.route('/users', endpoint='all_users')
class AdminManagementResource(Resource):
    """Shows a list of all users"""
    @api.doc('get list of users')
    @jwt_required
    @admin_auth
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

@ns_admin.route('/users/<string:user_id>', endpoint='user')
class AdminManagementItem(Resource):
    """Show a single todo item and lets you delete them"""
    @api.response(200, 'success')
    @api.doc('get user by id')
    @jwt_required
    @admin_auth
    def get(self, user_id):
        """Returns a user by a given id"""
        abort_if_doesnt_exists(user_id)
        response = {
            "data": store.get_user(user_id)
        }
        return response, 200

    @api.doc('delete user')
    @jwt_required
    @admin_auth
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
    """Login resource"""
    @api.doc('login user')
    @api.response(201, 'Login successful')
    @api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        data = request.json
        return Auth.login_user(data=data)

@ns_auth.route('/refresh_token')
class TokenRefresh(Resource):
    """Token refresh resource"""
    @jwt_refresh_token_required
    @api.doc('token refresh')
    @api.response(201, 'Token refreshed successfully')
    def post(self):
        """refresh the token"""
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            response = {
                'status': 'success',
                'message': 'token refreshed successfully',
                'access_token': access_token
            }
            return response, 201
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not create refresh token: {}'.format(e)
            }
            return response, 500


@ns_auth.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @api.doc('logout user')
    @jwt_required
    @api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        jti = get_raw_jwt()['jti']
        try:
            Auth.logout_user(jti)
            response = {
                'status': 'success',
                'message': 'Access token has been revoked, you are now logged out'
            }
            return response, 200
        except Exception as e:
            return {
                'message': 'could not generate access token: {}'.format(e)
            }
    
@ns_auth.route('/logout_refresh')
class UserLogoutResourceRefresh(Resource):
    """Logout refresh resource"""
    @jwt_refresh_token_required
    @api.doc('Logout refresh resource')
    @api.response(201, 'Success')
    def post(self):
        """Logout refresh token"""
        jti = get_raw_jwt()['jti']
        try:
            Auth.logout_user(jti)
            response = {
                'status': 'success',
                'message': 'Refresh token has been revoked'
            }
            return response, 200
        except:
            return {
                'message': 'could not generate refresh token'
            }