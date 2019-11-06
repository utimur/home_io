from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField

from ....models import Device


class DeviceSchema(Schema):
    model = Device

    uuid = fields.UUID(
        missing=None
    )

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=32),
            validate.Regexp(r'(^|,)[\w]+(,|$)', 0)
        ]
    )

    registered_at = ArrowField()

    owner_id = fields.Nested(
        'UserSchema',
        many=False
    )
