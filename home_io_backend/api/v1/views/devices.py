from uuid import uuid4

from . import parser
from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema
from ..view_decorators import json_mimetype_required
from ....models import Device, db


@api.route("/devices", methods=['POST'])
@json_mimetype_required
@parser.use_kwargs(DeviceCreateSchema, locations=('json',))
def create_new_device(uuid, name, owner_id):
    device = Device.query.filter(
        Device.name == name
    ).one_or_none()
    if device is not None:
        return DeviceAlreadyExistResponse()

    if uuid is None:
        uuid = uuid4()

    device = Device(
        uuid=uuid,
        name=name,
        owner_id=owner_id,
    )
    db.session.add(device)
    db.session.commit()
    return DeviceResponse(device)
