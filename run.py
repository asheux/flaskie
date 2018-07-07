import logging.config
import os
import sys
from getpass import getpass
from flask import Flask, Blueprint
from flask_script import Manager
from flask_jwt_extended import JWTManager
from flaskie import settings
from flaskie.api.v1.auth.errors import check_valid_email
from flaskie.api.restplus import api
from flaskie.api.v1.auth.collections import store
from flaskie.api.restplus import blueprint
from flaskie.api.v1.models import BlackListToken, User
from flaskie.database import db
from flaskie.api.v1.auth.routes.userroutes import ns as user_namespace

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    flask_app.config['JWT_BLACKLIST_ENABLED'] = settings.JWT_BLACKLIST_ENABLED
    flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = settings.JWT_BLACKLIST_TOKEN_CHECKS

def initialize_app(flask_app):
    configure_app(flask_app)
    jwt = JWTManager(flask_app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return BlackListToken.check_blacklist(jti)

    api.init_app(blueprint)
    api.add_namespace(user_namespace)
    flask_app.register_blueprint(blueprint)

def main():
    initialize_app(app)

    log.info('Starting development server at http://{}/api/v1/'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()