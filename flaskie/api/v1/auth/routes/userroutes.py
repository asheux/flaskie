import logging
from flask_bcrypt import Bcrypt
from flask import request, jsonify
from flask_restplus import Resource
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user_register, page_of_users, Pagination, user_login
from ..collections import store
from ..errors import abort_if_doesnt_exists

flask_bcrypt = Bcrypt()
log = logging.getLogger(__name__)
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
    @api.doc('Get a list of users')
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

@ns.route('/login')
class UserLoginResource(Resource):
    @api.response(201, 'Login successful')
    @api.expect(user_login)
    def post(self):
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
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in as {}'.format(user['name'])
                }
                return response, 200

        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not login: {}, try again.'.format(e)
            }
            return response, 500


@ns_admin.route('/login')
class UserLoginResource(Resource):
    @api.response(201, 'Login successful')
    @api.expect(user_login)
    def post(self):
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
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in as {}'.format(user['name'])
                }
                return response, 200

        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not login: {}, try again.'.format(e)
            }
            return response, 500