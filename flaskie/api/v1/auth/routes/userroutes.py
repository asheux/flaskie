import logging

from flask import request
from flask_restplus import Resource
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user, page_of_users
from ..collections import create_user, get_all_users

log = logging.getLogger(__name__)
ns = api.namespace('users', description='User operations')

@ns.route('/')
class UsersCollection(Resource):
    @api.doc('Get a list of users')
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_users)
    def get(self):
        """Return list of users"""
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        users_query = get_all_users
        users_page = users_query.paginate(page, per_page, error_out=False)

        return users_page
    @api.doc(pagination_arguments)
    @api.expect(user)
    @api.marshal_with(user, code=201)
    def post(self):
        """Creates a new user"""
        result = request.json
        name = result.get('name')
        username = result.get('username')
        email = result.get('email')
        password = result.get('password')
        role = result.get('role')

        user = User(name, username, email, password, role)
        new_user = create_user(user)
        response = {
            "status": "success",
            "message": "new user created"
        }
        return response, 201