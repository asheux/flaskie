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
          description='A user api that handles user authentication storing data in memory structure')
        

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500