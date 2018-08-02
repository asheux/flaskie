import logging.config
import os
from urllib.parse import urlparse
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from getpass import getpass
from flask_restplus import Api
from flask import Flask, Blueprint
from flask_script import Manager
from flask_jwt_extended import JWTManager
from flaskie import settings
from flaskie.api.restplus import blueprint, api, authorizations
from flaskie.database import db
from flaskie.api.v1.auth.routes.userroutes import ns as user_namespace

class Database:
    connection = None
    cursor = None
    app = None

    def init_app(self, app):
        self.app = app
        self.url = urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            dbname=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

v2_db = Database()
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
    
v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')
v2_api = Api(v2_blueprint, authorizations=authorizations, version='1.1', title='V2 of user requests API',
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

def configure_app(flask_app):
    from flaskie.api.v2.app.resources import ns as v2_user_namespace
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    flask_app.config['JWT_BLACKLIST_ENABLED'] = settings.JWT_BLACKLIST_ENABLED
    flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = settings.JWT_BLACKLIST_TOKEN_CHECKS
    flask_app.config['TESTING'] = settings.TESTING
    flask_app.config['DATABASE_NAME'] = settings.DATABASE_NAME
    flask_app.config['DATABASE_USER'] = settings.DATABASE_USER
    flask_app.config['DATABASE_PASSWORD'] = settings.DATABASE_PASSWORD
    flask_app.config['DATABASE_HOST'] = settings.DATABASE_HOST

def initialize_app(flask_app):
    configure_app(flask_app)
    jwt = JWTManager(flask_app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        from flaskie.api.v1.models import BlackListToken
        jti = decrypted_token['jti']
        return BlackListToken.check_blacklist(jti)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        from flaskie.api.v2.models import BlackList
        return BlackList.get_by_field(field='jti', value=token['jti']) is not None

    jwt._set_error_handler_callbacks(api)
    jwt._set_error_handler_callbacks(v2_api)
    flask_app.register_blueprint(v2_blueprint)
    flask_app.register_blueprint(blueprint)
    v2_db.init_app(flask_app)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    initialize_app(app)

    log.info('Starting development server at http://{}'.format(settings.FLASK_SERVER_NAME))

    return app