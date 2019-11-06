'''This module contains view decorators.
It can be helpful for mimetype check and etc.'''

import functools

from flask import request

from ..common.responses import *


def json_mimetype_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return JsonMimetypeRequiredResponse()
        return view(*args, **kwargs)
    return wrapper


def mimetype_required(*mimetypes):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if request.mimetype not in mimetypes:
                raise BadRequestResponse(*mimetypes)
            return view(*args, **kwargs)
        return wrapper
    return decorator
