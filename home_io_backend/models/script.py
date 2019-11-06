import arrow
from sqlalchemy_utils import ArrowType

from . import db


class Script(db.Model):

    __tablename__ = 'script'

    baked_query = db.bakery(lambda session: session.query(Script))

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    name = db.Column(
        db.String(64),
        nullable=False
    )

    tag = db.Column(
        db.String(64),
        nullable=False
    )

    src_path = db.Column(
        db.String(4096),
        nullable=False
    )

    calls = db.Column(
        db.Integer,
        default=0
    )

    runtime = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )

    updated_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
