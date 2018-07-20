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
from flaskie.api.restplus import v2_api
from flaskie.api.v2.app.serializers import (
    user_register, 
    page_of_users, 
    Pagination, 
    user_login,
    requests,
    request_status
)
from flaskie import settings
from flaskie.api.v2.models import User, BlackList
from ..app.errors import check_valid_email, user_is_valid, abort_if_doesnt_exists

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
            access_token = create_access_token(data['username'])
            refresh_token = create_refresh_token(data['username'])
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
                access_token = create_access_token(user['username'])
                refresh_token = create_refresh_token(user['username'])
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


@ns_auth.route('/logout')
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
            return {
                'message': 'could not generat access token: {}'.format(e)
            }
    
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
            return {
                'message': 'could not generat refresh token: {}'.format(e)
            }

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
            user = User.get_by_field(field='username', value=current_user)
            if user is not None:
                response = {
                    'status': 'success',
                    'data': {
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
            return {
                'message': '{}'.format(e)
            }

@ns.route('/<int:user_id>') 
@v2_api.response(404, 'User with the given id not found')
class ModifyUser(Resource):
    @v2_api.doc(pagination_arguments)
    @jwt_required
    @v2_api.response(200, 'User updated successfully')
    @v2_api.expect(user_register, validate=True)
    def put(self, user_id):
        """Updates user details"""
        pass

@ns_admin.route('/all_users', endpoint='all_users')
class AdminManagementResource(Resource):
    """Shows a list of all users"""
    @v2_api.doc('get list of users')
    @jwt_required
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
        pass
    
    @jwt_required
    @v2_api.doc('Request resource')
    @v2_api.response(200, 'success')
    def get(self):
        """get all requests for this particular user"""
        pass

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
        pass

    @jwt_required
    @v2_api.doc('Modify request resource')
    @v2_api.response(200, 'Successfully updated')
    @v2_api.expect(requests)
    def put(self, request_id):
        """Modifies a request with the given id"""
        # abort_if_request_doesnt_exists(request_id)
        pass
    
@ns_admin.route('/all_requests')
class AdminManageRequests(Resource):
    @jwt_required
    @v2_api.doc('Get all requests')
    @v2_api.response(200, 'success')
    def get(self):
        """Get all the request from the db"""
        pass

@ns_admin.route('/all_requests/<int:request_id>')
class AdminReactsToRequest(Resource):
    """Modify a request by responsing to it"""
    @jwt_required
    @v2_api.doc('Modify a given given request for a user')
    @v2_api.response(200, 'successfully updated')
    @v2_api.expect(request_status)
    def put(self, request_id):
        """Modify a request for a user"""
        pass