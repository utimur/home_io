from marshmallow import fields, Schema
from marshmallow_arrow import ArrowField

from ....models import Device, DeviceLog


class DeviceLogSchema(Schema):

    model = DeviceLog

    id = fields.Integer()

    log = fields.Raw(
        required=True
    )

    created_at = ArrowField()

    device_uuid = fields.UUID(
        required=True,
        validate=[
            lambda dev_id: Device.query.get(dev_id) is not None
        ]
    )
