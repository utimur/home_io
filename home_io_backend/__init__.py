import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

from ..config import Config

# create app and configure it
# NOTE: config file depends on build type (dev, test, prod)
app = Flask(__name__)
app.config.from_object(Config)

# register HTTP error handlers
with app.app_context():
    from .api.common.error_handlers import *

# setup token manager
jwt = JWTManager(app)

# import api dependencies
from .api.v1 import api
from .api.v1.views import *

# bind api blueprints
app.register_blueprint(api, url_prefix='/api/v1')

# import db models
from .models import *

# initialize database connection
db.init_app(app)
app.db = db
with app.app_context():
    app.db.session.enable_baked_queries = True

# setup migrations
# set custom migration folder
migrations_dir = os.environ.get('MIGRATIONS_DIR')
Migrate(app, db, directory=migrations_dir)

# create database if not exists
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])
