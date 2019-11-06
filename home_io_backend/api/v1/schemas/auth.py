from marshmallow import fields, Schema, validate


class LoginSchema(Schema):
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r'[\w]+')
        ]
    )

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r'[\w]+')
        ]
    )
