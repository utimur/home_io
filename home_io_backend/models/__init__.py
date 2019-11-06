from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import baked

db = SQLAlchemy()
db.bakery = baked.bakery()

bcrypt = Bcrypt()

from .user import User
from .device import Device
from .device_log import DeviceLog
from .device_task import DeviceTask
from .script import Script

__all__ = [
    'db',
    'User',
    'Device',
    'DeviceLog',
    'DeviceTask',
    'Script'
]
