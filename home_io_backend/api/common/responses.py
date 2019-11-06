'''This module contains common JSON responses.'''

__all__ = [
    'JsonApiResponse',
    'JsonApiErrorResponse',
    'JsonMimetypeRequiredResponse',
    'BadRequestResponse',
    'JsonValidationErrorResponse',
    'InvalidBodyResponse',
    'MethodNotAllowedResponse',
    'NotFoundResponse',
    'PaginateResponse'
]

import json

from flask import Response
from sqlalchemy import bindparam

from ...models import db


class JsonApiResponse(Response):
    '''Custom JSON response.
    This is a base class for other API responses.'''
    def __init__(self, response, status):
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class JsonApiErrorResponse(Response):
    '''Custom JSON error response.
    This is a base class for other API responses.'''
    def __init__(self, error_code, status, body=None):
        response = {
            'error_code': error_code
        }
        if body is not None:
            response['data'] = body
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class PaginateResponse(JsonApiResponse):
    def __init__(self, bq, schema, page=0, per_page=None, bq_params=None):
        paging_params = {}
        if per_page is not None:
            bq += lambda q: q\
                .limit(bindparam('page_size'))\
                .offset(bindparam('page_offset'))

            paging_params.update({
                'page_size': per_page,
                'page_offset': page * per_page
            })

        if bq_params is None:
            bq_params = paging_params
        else:
            bq_params.update(paging_params)

        query = bq(db.session()).params(bq_params).all()

        response = {
            'data': schema.dump(query),
            'page': page,
            'per_page': per_page
        }
        super().__init__(response, 200)


class JsonMimetypeRequiredResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('JSON_MIMETYPE_REQUIRED', 400)


class JsonValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('JSON_VALIDATION_ERROR', 400)


class MimetypeValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('MIMETYPE_VALIDATION_ERROR', 400)


class BadRequestResponse(JsonApiErrorResponse):
    def __init__(self, body):
        super().__init__('BAD_REQUEST', 400, body=body)


class NotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('NOT_FOUND', 404)


class MethodNotAllowedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('METHOD_NOT_ALLOWED', 405)


class InvalidBodyResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('INVALID_BODY_ERROR', 422)
