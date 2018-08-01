import logging
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    get_raw_jwt
)
from flaskie.api.v1.auth.parsers import pagination_arguments
from flaskie import v2_api
from flaskie.api.v2.app.serializers import (
    user_register, 
    page_of_users, 
    Pagination, 
    user_login,
    requests,
    request_status,
    modify_user
)
from flaskie import settings
from flaskie.api.v2.models import User, BlackList, Requests
from ..app.errors import (
    check_valid_email,
    user_is_valid,
    abort_if_doesnt_exists,
    abort_if_requests_doesnt_exists
)
from .decorators import admin_auth

flask_bcrypt = Bcrypt()
log = logging.getLogger(__name__)
ns_auth = v2_api.namespace('auth', description='Authentication operations')
ns = v2_api.namespace('user', description='User operations')
ns_admin = v2_api.namespace('admin', description='Admin Management')


@ns_auth.route('/registration')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @v2_api.doc(pagination_arguments)
    @v2_api.response(201, 'User created successfully')
    @v2_api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        errors = user_is_valid(data)
        if check_valid_email(data['email']) is None:
            response = {
                'status': 'error',
                'message': 'Not a valid email address, please try again'
            }
            return response, 403
        elif errors:
            response = {
                'status': 'error',
                'message': errors
            }
            return response, 401
        else:
            user = User(data['name'], data['username'], data['email'], data['password'])
            user.insert()
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            response = {
                'status': 'success',
                'message': 'user created successfully',
                'Authorization': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
            return response, 201

@ns_auth.route('/login_access')
class UserLoginResource(Resource):
    """Login resource"""
    @v2_api.doc('login user')
    @v2_api.response(201, 'Login successful')
    @v2_api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        try:
            data = request.json
            user = User.get_by_field(field='username', value=data.get('username'))
            if not user:
                response = {
                    'status': 'fail',
                    'message': 'The username you provided does not exist in the database'
                }
                return response, 404
            elif not flask_bcrypt.check_password_hash(user['password_hash'], data.get('password')):
                response = {
                    'status': 'fail',
                    'message': 'The password you provided did not match the database password'
                }
                return response, 401
            else:
                access_token = create_access_token(user['id'])
                refresh_token = create_refresh_token(user['id'])
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in as {}'.format(user['name']),
                    'Authorization': {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }
                return response, 201
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not login: {}, try again'.format(e)
            }
            return response, 500

@ns_auth.route('/token_refresh')
class TokenRefresh(Resource):
    """Token refresh resource"""
    @jwt_refresh_token_required
    @v2_api.doc('token refresh')
    @v2_api.response(201, 'Token refreshed successfully')
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
                'message': 'could not create refresh token: {}'.format(e)
            }
            return response, 500


@ns_auth.route('/logout_user')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @v2_api.doc('logout user')
    @jwt_required
    @v2_api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        jti = get_raw_jwt()['jti']
        try:
            blacklist_token = BlackList(jti=jti)
            blacklist_token.insert()
            response = {
                'status': 'success',
                'message': 'Access token has been revoked, you are now logged out'
            }
            return response, 200
        except Exception as e:
            response = {
                'message': 'could not generat access token: {}'.format(e)
            }
            return response
    
@ns_auth.route('/logout_refresh_token')
class UserLogoutResourceRefresh(Resource):
    """Logout refresh resource"""
    @jwt_refresh_token_required
    @v2_api.doc('Logout refresh resource')
    @v2_api.response(201, 'Success')
    def post(self):
        """Logout refresh token"""
        jti = get_raw_jwt()['jti']
        try:
            blacklist_token = BlackList(jti=jti)
            blacklist_token.insert()
            response = {
                'status': 'success',
                'message': 'Refresh token has been revoked'
            }
            return response, 200
        except Exception as e:
            response = {
                'message': 'could not generat refresh token: {}'.format(e)
            }
            return response

@ns.route('/current')
class UserItem(Resource):
    """Show a single todo item and lets you delete them"""
    @v2_api.response(200, 'success')
    @jwt_required
    @v2_api.doc('user gets their details')
    def get(self):
        """Returns a logged in user's details"""
        current_user = get_jwt_identity()
        try:
            user = User.get_by_field(field='id', value=current_user)
            if user is not None:
                response = {
                    'status': 'success',
                    'data': {
                        'id': user['id'],
                        'name': user['name'],
                        'username': user['username'],
                        'email': user['email'],
                        'admin': user['admin'],
                        'password': user['password_hash'],
                        'registered_on': user['registered_on']
                    }
                }
                return response, 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'current user is None'
                }
                return response, 404
        except Exception as e:
            response = {
                'message': '{}'.format(e)
            }
            return response

@ns.route('/<int:user_id>') 
@v2_api.response(404, 'User with the given id not found')
class ModifyUser(Resource):
    @v2_api.doc(pagination_arguments)
    @jwt_required
    @v2_api.response(200, 'User updated successfully')
    @v2_api.expect(modify_user, validate=True)
    def put(self, user_id):
        """Updates user details"""
        user = User.get_item_by_id(user_id)
        abort_if_doesnt_exists(user_id)
        if user['id'] != get_jwt_identity():
            response = {
                'status': 'fail',
                'message': 'You are no allowed to update someone else data'
            }
            return response, 401
        data = request.json
        user['name'] = data['name']
        user['username'] = data['username']
        user['email'] = data['email']
        if user['admin'] == True:
            user = User(
                user['name'], 
                user['username'], 
                user['email'],
                password=user['password_hash'],
                registered_on=user['registered_on'],
                admin=True
            )
            user.updateuser(user_id)
            response = {
                'status': 'success',
                'message': user.toJSON()
            }
            return response, 201
        user = User(
            user['name'], 
            user['username'], 
            user['email'],
            password=user['password_hash'],
            registered_on=user['registered_on']
        )
        user.updateuser(user_id)
        response = {
            'status': 'success',
            'message': user.toJSON()
        }
        return response, 201

@ns_admin.route('/all_users', endpoint='all_users')
class AdminManagementResource(Resource):
    """Shows a list of all users"""
    @v2_api.doc('get list of users')
    @jwt_required
    @admin_auth
    @v2_api.expect(pagination_arguments)
    def get(self):
        """Return list of users"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        all_users = User.get_all()
        paginate = Pagination(page, per_page, len(all_users))
        if all_users == []:
            response = {
                'message': 'There are no users in the database yet'
            }
            return response, 404
        response = {
            "status": 'success',
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total_user": paginate.total_count,
            "data": all_users
        }
        return response, 200

@ns_admin.route('/all_users/<int:user_id>', endpoint='user')
@v2_api.response(404, 'User with the given id not found')
class AdminManagementItem(Resource):
    """Show a single todo item and lets you delete them"""
    @v2_api.response(200, 'success')
    @v2_api.doc('get user by id')
    @jwt_required
    @admin_auth
    def get(self, user_id):
        """Returns a user by a given id"""
        user = User.get_item_by_id(user_id)
        abort_if_doesnt_exists(user_id)
        response = {
            'status': 'success',
            'data': user
        }
        return response, 200

@ns.route('/my_requests')
class UserRequestsResource(Resource):
    """Request resource endpoint"""
    @jwt_required
    @v2_api.doc('Request resource')
    @v2_api.response(201, 'Successfully created')
    @v2_api.expect(requests)
    def post(self):
        """Creates a new request"""
        data = request.json
        try:
            new_request = Requests(
                data['requestname'], 
                data['description'],
                created_by=get_jwt_identity()
            )
            new_request.insert()

            response = {
                'status': 'success',
                'message': 'Successfully created a request'
            }
            return response, 201
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'could not create request: {}'.format(e)
            }
            return response
    
    @jwt_required
    @v2_api.doc('Request resource')
    @v2_api.response(200, 'success')
    def get(self):
        """get all requests for this particular user"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = Requests.get_all()
        requests = [req for req in data if req['created_by'] == get_jwt_identity()]
        paginate = Pagination(page, per_page, len(requests))
        if requests == []:
            response = {
                'message': 'The current user has no requests in the db'
            }
            return response, 404
        response = {
            "status": 'success',
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total_user": paginate.total_count,
            "data": requests
        }
        return response, 200
        

@ns.route('/my_requests/<int:request_id>')
@v2_api.response(404, 'request with the given id not found')
class UserRequestItem(Resource):
    """Single user request resource"""
    @jwt_required
    @v2_api.doc('Single request resource')
    @v2_api.response(200, 'Success')
    def get(self, request_id):
        """Get a request by a specific user"""
        # abort_if_request_doesnt_exists(request_id)
        requestt = Requests.get_item_by_id(request_id)
        abort_if_requests_doesnt_exists(request_id)
        if requestt['created_by'] == get_jwt_identity():
            response = {
                'status': 'success',
                'data': requestt
            }
            return response, 200
        else:
            response = {
                'status': 'fail',
                'message': 'You are no allowed to view or update this request'
            }
            return response, 401

    @jwt_required
    @v2_api.doc('Modify request resource')
    @v2_api.response(200, 'Successfully updated')
    @v2_api.expect(requests)
    def put(self, request_id):
        """Modifies a request with the given id"""
        # abort_if_request_doesnt_exists(request_id)
        my_request = Requests.get_item_by_id(request_id)
        abort_if_requests_doesnt_exists(request_id)
        if my_request['created_by'] != get_jwt_identity():
            response = {
                'status': 'fail',
                'message': 'You are no allowed to view or update this request'
            }
            return response, 401
        elif my_request['status'] != settings.STATUS_P:
            response = {
                'status': 'fail',
                'message': 'Sorry, only pending requests can be modified'
            }
            return response, 403
        data = request.json
        my_request['requestname'] = data['requestname']
        my_request['description'] = data['description']
        my_request = Requests(
            my_request['requestname'], 
            my_request['description'], 
            date_created=my_request['date_created']
        )
        my_request.updaterequest(request_id)
        response = {
            'status': 'success',
            'message': 'Request successfully updated'
        }
        return response, 201
    
@ns_admin.route('/all_requests')
class AdminManageRequests(Resource):
    @jwt_required
    @admin_auth
    @v2_api.doc('Get all requests')
    @v2_api.response(200, 'success')
    def get(self):
        """Get all the request from the db"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = Requests.get_all()
        paginate = Pagination(page, per_page, len(data))
        if data == []:
            response = {
                'message': 'There are no users in the database yet'
            }
            return response, 404
        response = {
            "status": 'success',
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total_user": paginate.total_count,
            "data": data
        }
        return response, 200

@ns_admin.route('/all_requests/<int:request_id>')
class AdminReactsToRequest(Resource):
    """Modify a request by responsing to it"""
    @jwt_required
    @admin_auth
    @v2_api.doc('Modify a given given request for a user')
    @v2_api.response(200, 'successfully updated')
    @v2_api.expect(request_status)
    def put(self, request_id):
        """Modify a request for a user"""
        req = Requests.get_item_by_id(request_id)
        data = request.json
        abort_if_requests_doesnt_exists(request_id)
        valid_statuses = {
            'approve': settings.STATUS_A,
            'reject': settings.STATUS_R,
            'resolve': settings.STATUS_S
        }
        if data['status'] not in valid_statuses.keys():
            response = {
                'status': 'fail',
                'message': 'Not a valid status name, please try (approve, reject, resolve)'
            }
            return response, 400
        elif data['status'] == 'approve' and req['status'] != settings.STATUS_P:
            response = {
                'status': 'fail',
                'message': 'Sorry, only pending requests can be reacted on'
            }
            return response, 400
        req['status'] = valid_statuses[data['status']]
        req = Requests(
            requestname=req['requestname'], 
            description=req['description'], 
            date_created=req['date_created'],
            status=req['status']
        )
        req.updaterequest(request_id)
        response = {
            'status': 'success',
            'message': 'Request successfully {} this request'.format(valid_statuses[data['status']])
        }
        return response, 201