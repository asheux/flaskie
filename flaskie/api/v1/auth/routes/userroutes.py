import logging

from flask import request, jsonify
from flask_restplus import Resource
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user, page_of_users, Pagination
from ..collections import store
from ..errors import abort_if_doesnt_exists

log = logging.getLogger(__name__)
ns = api.namespace('users', description='User operations')

@ns.route('/')
class UsersCollection(Resource):
    '''Shows a list of all users, and lets you POST to add new users'''
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

    @api.doc(pagination_arguments)
    @api.response(201, 'User created successfully')
    @api.expect(user, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return store.create_user(data=data)

@ns.route('/<int:user_id>')
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

    @api.doc(pagination_arguments)
    @api.response(200, 'User updated successfully')
    @api.expect(user, validate=True)
    def put(self, user_id):
        """Updates user details"""
        abort_if_doesnt_exists(user_id)
        data = request.json
        return store.update_user(user_id, data)

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
