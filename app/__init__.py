from flask import Flask
from flask_restful import Api
from conf.config import config
from .auth import auth as auth_blueprint

def create_app(config_name):
    """This is the application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)

    #Registering blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/users")

    return app
