import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    # optei por nao usar variaveis de ambiente para tornar o teste mais simples
    POSTGRES_URL = "127.0.0.1:5432"
    POSTGRES_USER = "azk4n"
    POSTGRES_PW = ""
    POSTGRES_DB = "netsupdb"

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PW,
        url=POSTGRES_URL,
        db=POSTGRES_DB
    )
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
