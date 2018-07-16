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

log = logging.getLogger(__name__)
ns_auth = v2_api.namespace('auth', description='Authentication operations')
ns = v2_api.namespace('user', description='User operations')
ns_admin = v2_api.namespace('admin', description='Admin Management')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @v2_api.doc(pagination_arguments)
    @v2_api.response(201, 'User created successfully')
    @v2_api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        pass

@ns.route('')
class UserItem(Resource):
    """Show a single todo item and lets you delete them"""
    @v2_api.response(200, 'success')
    @jwt_required
    @v2_api.doc('user gets their details')
    def get(self):
        """Returns a logged in user's details"""
        pass

@ns.route('/<string:user_id>') 
@v2_api.response(404, 'User with the given id not found')
class ModifyUser(Resource):
    @v2_api.doc(pagination_arguments)
    @jwt_required
    @v2_api.response(200, 'User updated successfully')
    @v2_api.expect(user_register, validate=True)
    def put(self, user_id):
        """Updates user details"""
        pass

@ns_admin.route('/users', endpoint='all_users')
class AdminManagementResource(Resource):
    """Shows a list of all users"""
    @v2_api.doc('get list of users')
    @jwt_required
    @v2_api.expect(pagination_arguments)
    def get(self):
        """Return list of users"""
        pass

@ns_admin.route('/users/<string:user_id>', endpoint='user')
@v2_api.response(404, 'User with the given id not found')
class AdminManagementItem(Resource):
    """Show a single todo item and lets you delete them"""
    @v2_api.response(200, 'success')
    @v2_api.doc('get user by id')
    @jwt_required
    def get(self, user_id):
        """Returns a user by a given id"""
        pass
        

@ns_auth.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @v2_api.doc('login user')
    @v2_api.response(201, 'Login successful')
    @v2_api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        pass

@ns_auth.route('/refresh_token')
class TokenRefresh(Resource):
    """Token refresh resource"""
    @jwt_refresh_token_required
    @v2_api.doc('token refresh')
    @v2_api.response(201, 'Token refreshed successfully')
    def post(self):
        """refresh the token"""
        pass


@ns_auth.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @v2_api.doc('logout user')
    @jwt_required
    @v2_api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        pass
    
@ns_auth.route('/logout_refresh')
class UserLogoutResourceRefresh(Resource):
    """Logout refresh resource"""
    @jwt_refresh_token_required
    @v2_api.doc('Logout refresh resource')
    @v2_api.response(201, 'Success')
    def post(self):
        """Logout refresh token"""
        pass

@ns.route('/requests')
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

@ns.route('/requests/<int:request_id>')
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
    
@ns_admin.route('/requests')
class AdminManageRequests(Resource):
    @jwt_required
    @v2_api.doc('Get all requests')
    @v2_api.response(200, 'success')
    def get(self):
        """Get all the request from the db"""
        pass

@ns_admin.route('/requests/<int:request_id>')
class AdminReactsToRequest(Resource):
    """Modify a request by responsing to it"""
    @jwt_required
    @v2_api.doc('Modify a given given request for a user')
    @v2_api.response(200, 'successfully updated')
    @v2_api.expect(request_status)
    def put(self, request_id):
        """Modify a request for a user"""
        pass