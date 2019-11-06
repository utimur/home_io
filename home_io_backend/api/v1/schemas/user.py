from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField

from .device import DeviceSchema
from .script import ScriptSchema
from ....models import User


class UserSchema(Schema):

    model = User

    id = fields.Integer()

    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r'(^|,)[\w]+(,|$)', 0)
        ]
    )

    email = fields.Email(
        required=True,
        validate=[
            validate.Length(min=8, max=64)
        ]
    )

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r'[\w]+')
        ]
    )

    created_at = ArrowField()

    devices = fields.Nested(
        DeviceSchema,
        many=True
    )

    scripts = fields.Nested(
        ScriptSchema,
        many=True
    )
