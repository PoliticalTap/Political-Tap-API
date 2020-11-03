import os

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    VOTESMART_SECRET = os.environ.get("VOTESMART_SECRET")


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    Testing = True
    SESSION_COOKIE_SECURE = False