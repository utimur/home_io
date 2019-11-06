import arrow
from sqlalchemy_utils import ArrowType

from . import db, bcrypt
from .device import Device
from .script import Script


class User(db.Model):
    __tablename__ = 'user'

    baked_query = db.bakery(lambda session: session.query(User))

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)

    _password_hash = db.Column(db.Binary(72), nullable=False)
    password = property()

    @password.setter
    def password(self, value):
        self._password_hash = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        return bcrypt.check_password_hash(self._password_hash, value)

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )

    devices = db.relationship(
        Device,
        backref='user',
        cascade='all, delete-orphan'
    )

    scripts = db.relationship(
        Script,
        backref='user',
        cascade='all, delete-orphan'
    )
