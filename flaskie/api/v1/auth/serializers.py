from flask_restplus import fields
from flaskie.api.restplus import api

user = api.model('User API', {
    'user_id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='User fullname'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='The user\'s email address'),
    'password': fields.String(required=True, description='The users secret password'),
    'registered_on': fields.DateTime,
    'role': fields.String(required=True, description='The role of users i the application'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_users = api.inherit('Page of users', pagination, {
    'items': fields.List(fields.Nested(user))
})
