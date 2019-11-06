from webargs.flaskparser import FlaskParser

parser = FlaskParser()

# noqa
from ..error_handlers import handle_marshmallow_error

from .auth import *
from .devices import *
from .scripts import *
from .users import *
