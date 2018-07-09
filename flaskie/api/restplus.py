import logging
import traceback
from flask import Blueprint
from flask_restplus import Api
from .. import settings

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
log = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, authorizations=authorizations, version='1.0', title='User API',
          description=(
            "A user api that handles user authentication storing data in memory structure.\n\n"
            "##The demo features:\n"
            "* Users can create an account and log in.\n"
            "* Users can update their details\n"
            "* Users can delete their account\n"
            "* Users can view the account details\n"
            "* Admin can view all users in the app.\n"
            "* Admin can view his/her details.\n"
            "* Admin can delete a user with the specified user_id.\n"
            "* Admin can get a user with the specified user_id.\n"
            "* Admin can update a user with the specified user_id.\n"
            "* Role based permission system.\n"
            "* It is auto documented.\n"
            "* 77+% code coverage.\n\n"
            "##Exploring the demo.\n"
            "Create a new user at the 'POST /auth/user' endpoint. Get the user access token from the response."
            "Click the authorize button and add the token in the following format.\n\n"
            "`Bearer (jwt-token without the brackets)`\n\n"
            "There is also a built-in user:\n"
            "* `paulla` (administrator with all permissions) with password `mermaid`\n\n"
            "## Authorization token(with the help of)\n"
            "`Jwt-Extended`"
        ),
    )
        

@api.errorhandler
def default_error_handler(e):
    """Handles errors on the app at runtime"""
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500