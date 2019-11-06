import arrow
from sqlalchemy_utils import ArrowType, JSONType

from . import db


class DeviceLog(db.Model):
    __tablename__ = 'device_log'

    baked_query = db.bakery(lambda session: session.query(DeviceLog))

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        unique=True
    )

    log = db.Column(
        JSONType,
        nullable=False
    )

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow,
        index=True
    )

    device_uuid = db.Column(
        db.ForeignKey(
            'device.uuid',
            ondelete='CASCADE'
        ),
        nullable=False
    )
