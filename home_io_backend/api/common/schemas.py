__all__ = [
    'PaginationSchema'
]

from marshmallow import fields, Schema, validate


class PaginationSchema(Schema):
    page = fields.Integer(
        missing=0,
        validate=[
            validate.Range(min=0)
        ]
    )

    per_page = fields.Integer(
        missing=None,
        validate=[
            validate.Range(min=0)
        ]
    )


PaginationSchema = PaginationSchema()
