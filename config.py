import os
basedir = os.path.abspath(os.path.dirname(__file__))

#common config for all environment
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DESIGNMIXER'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DESIGNMIXER_MAIL_SUBJECT_PREFIX = '[DesignerMixer]'
    DESIGNMIXER_MAIL_SENDER = 'DesignerMixer Admin <hi@maxlee.im>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

#config for specifically environment, inherit from the Config class
class DevelopmentConfig(Config): DEBUG = True
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config): TESTING = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#dictionary for create_app to choose config
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    #DevelopmentConfig is the default config
    'default': DevelopmentConfig
}
