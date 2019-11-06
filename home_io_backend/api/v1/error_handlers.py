__all__ = [
    'handle_marshmallow_error'
]

from marshmallow.exceptions import MarshmallowError

from .views import parser


@parser.error_handler
def handle_marshmallow_error(error, req, schema, status_code, headers):
    raise MarshmallowError(error)
