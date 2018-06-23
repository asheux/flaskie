import logging

from flask import request, jsonify
from flask_restplus import Resource
from ..parsers import pagination_arguments
from flaskie.api.restplus import api
from flaskie.api.v1.models import User
from ..serializers import user, page_of_users, Pagination
from ..collections import create_user, get_all_users

log = logging.getLogger(__name__)
ns = api.namespace('users', description='User operations')

@ns.route('/')
class UsersCollection(Resource):
    @api.doc('Get a list of users')
    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_users)
    def get(self):
        """Return list of users"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        users_query = get_all_users()
        paginate = Pagination(page, per_page, len(users_query))
        result = [{k:v for k, v in [(k,v) for item in users_query for k, v in item.items()]}]
        response = {
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total": paginate.total_count,
            "data": result
        }
        return response, 200

    @api.doc(pagination_arguments)
    @api.response(201, 'User created successfully')
    @api.expect(user, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return create_user(data=data)