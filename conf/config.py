import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    """The main app configurations"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'security is delicate')
    FLASKIE_ADMIN = os.environ.get('FLASKIE_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Configuration):
    """Configuration for development server"""
    DEBUG = True

class TestingConfig(Configuration):
    """Testing configurations"""
    TESTING = True

class ProductionConfig(Configuration):
    """Production configurations"""
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

