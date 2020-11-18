import os

class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Votesmart API Keys 
    VOTESMART_SECRET = os.environ.get("VOTESMART_SECRET")

    # Twitter API keys
    TWITTER_KEY = os.environ.get("TWITTER_KEY")
    TWITTER_SECRET = os.environ.get("TWITTER_SECRET")
    TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    Testing = True
    SESSION_COOKIE_SECURE = False