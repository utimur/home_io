'''This module used to set error handlers for common HTTP errors.'''

from flask import current_app
from marshmallow.exceptions import MarshmallowError

from ..common.responses import *

__all__ = [
    'handle_bad_request',
    'handle_method_not_allowed',
    'handle_unprocessable_entity',
    'handle_not_found',
    'handle_validation_error'
]


@current_app.errorhandler(400)
def handle_bad_request(error):
    return BadRequestResponse()


@current_app.errorhandler(404)
def handle_not_found(error):
    return NotFoundResponse()


@current_app.errorhandler(405)
def handle_method_not_allowed(error):
    return MethodNotAllowedResponse()


@current_app.errorhandler(422)
def handle_unprocessable_entity(error):
    return InvalidBodyResponse()


@current_app.errorhandler(MarshmallowError)
def handle_validation_error(error):
    return BadRequestResponse(error.args[0].messages)
