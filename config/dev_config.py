class Config(object):
    DEBUG = True

    # NOTE: for development only!
    SECRET_KEY = 'a7527038916b46a2b79d65a0e6ee5d98'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@home_io_backend_postgres/home_io_backend'