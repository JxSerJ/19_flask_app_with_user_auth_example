from helpers.constants import DATABASE_PATH, USER_DATABASE_PATH, TOKEN_DATABASE_PATH


class Config(object):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_BINDS = {'users': f'sqlite:///{USER_DATABASE_PATH}',
                        'tokens': f'sqlite:///{TOKEN_DATABASE_PATH}'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 4, 'sort_keys': False}
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    REGENERATE_DB_ON_START = False
    REGENERATE_USER_DB_ON_START = False
