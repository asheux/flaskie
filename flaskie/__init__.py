import logging.config
import os
import sys
from getpass import getpass
from flask import Flask, Blueprint
from flask_script import Manager
from flask_jwt_extended import JWTManager
from flaskie import settings
from flaskie.api.restplus import api
from flaskie.api.restplus import blueprint, v2_blueprint
from flaskie.api.v1.models import BlackListToken
from flaskie.database import db
from flaskie.api.v2.app.database import Database
from flaskie.api.v1.auth.routes.userroutes import ns as user_namespace
from flaskie.api.v2.app.resources import ns as v2_user_namespace

v2_db = Database()
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
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
        jti = decrypted_token['jti']
        return BlackListToken.check_blacklist(jti)

    flask_app.register_blueprint(v2_blueprint)
    flask_app.register_blueprint(blueprint)
    v2_db.init_app(flask_app)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    initialize_app(app)

    log.info('Starting development server at http://{}'.format(settings.FLASK_SERVER_NAME))

    return app