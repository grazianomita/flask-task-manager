from os import getenv


class Config:
    TESTING = False
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


def get_config():
    if getenv("FLASK_ENV") == 'DEV':
        return DevConfig
    elif getenv("FLASK_ENV") == 'PROD':
        return ProdConfig
    else:
        return TestConfig
