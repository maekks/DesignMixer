import os
basedir = os.path.abspath(os.path.dirname(__file__))

#common config for all environment
class Config:
    SSL_DISABLE = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DESIGNMIXER'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DESIGNMIXER_MAIL_SUBJECT_PREFIX = '[DesignerMixer]'
    DESIGNMIXER_MAIL_SENDER = 'DesignerMixer Admin <hi@maxlee.im>'
    MIXER_ADMIN = os.environ.get('MIXER_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 20
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass

#config for specifically environment, inherit from the Config class
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.DESIGNMIXER_MAIL_SENDER,
            toaddrs=[cls.MIXER_ADMIN],
            subject=cls.DESIGNMIXER_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        from werkzeug.contrib.fixer import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

#dictionary for create_app to choose config
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    #DevelopmentConfig is the default config
    'default': DevelopmentConfig
}
