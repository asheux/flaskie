import logging
import traceback
from flask import Blueprint
from flask_restplus import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
log = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, authorizations=authorizations, version='1.0', title='User requests API',
          description=(
            "An api that handles user authentication and user requests storing data in memory structure.\n\n"
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