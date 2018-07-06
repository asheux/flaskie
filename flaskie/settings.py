import os

# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
FLASK_APP = 'run.py'
FLASK_DEBUG = True  # Do not use debug mode in production
SECRET_KEY = os.getenv('SECRET_KEY', 'i love hot ladies')

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = True
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_MASK_HEADER = 'Authorization'

# SQLAlchemy settings

# Jwt settings
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_SECRET_KEY = 'jwt-secret-string'