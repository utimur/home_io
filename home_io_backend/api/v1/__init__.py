from flask import Blueprint
from .jwt_management import *

api = Blueprint('api_v1', __name__)
