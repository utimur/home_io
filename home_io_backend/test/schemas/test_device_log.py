from uuid import uuid4

import arrow
import pytest
from marshmallow.exceptions import ValidationError

from ...api.v1.schemas import DeviceLogReadSchema, DeviceLogCreateSchema, DeviceLogUpdateSchema
from ...models import DeviceLog, User, Device


@pytest.fixture(scope='function')
def device_uuid(app, db):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(user)
        db.session.flush()

        device = Device(
            uuid=uuid4(),
            name='testdevice',
            owner_id=user.id
        )
        db.session.add(device)
        db.session.commit()
        return device.uuid


@pytest.fixture(scope='function')
def device_log(app, db):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(user)
        db.session.flush()

        device = Device(
            uuid=uuid4(),
            name='testdevice',
            owner_id=user.id
        )
        db.session.add(device)
        db.session.flush()

        device_log = DeviceLog(
            log={
                'test': 'log'
            }
        )
        device.device_logs.append(device_log)
        db.session.commit()


class TestDeviceLogReadSchema:
    def test_read(self, app, device_log):
        with app.app_context():
            dev_log = DeviceLog.query.all()[0]
            try:
                DeviceLogReadSchema.dump(dev_log)
            except ValidationError:
                assert False, 'Can`t be ValidationError'


class TestDeviceLogCreateSchema:
    @pytest.mark.parametrize(
        'device_id, log',
        (('ffebed83-957b-49e4-ba70-b1b1f53004ad', {'log': 'test'}),
         ('edec2e3c-30c7-475e-aa3b-44642cf7c5a0', {'another_log': 'loglog'}),
         ('febf8c05-6fc1-4834-8ee4-998420dd2d1a', {'access': 'success'}),)
    )
    def test_invalid_device_id(self, app, device_id, log):
        dev_log = {
            'device_uuid': device_id,
            'log': log
        }
        try:
            with app.app_context():
                DeviceLogCreateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'device_uuid' in e.messages


    @pytest.mark.parametrize(
        'log_id, created_at, device_id, log',
        ((1, arrow.now(), 'edec2e3c-30c7-475e-aa3b-44642cf7c5a0', {'key': 'value'}), )
    )
    def test_pass_not_allowed_keys(self, app, log_id, created_at, device_id, log):
        dev_log = {
            'id': log_id,
            'created_at': created_at,
            'device_uuid': device_id,
            'log': log,
        }
        try:
            with app.app_context():
                DeviceLogCreateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'log',
        ({'log': 'test'}, )
    )
    def test_valid_data(self, app, device_uuid, log):
        dev_log = {
            'device_uuid': device_uuid,
            'log': log,
        }
        try:
            with app.app_context():
                DeviceLogCreateSchema.load(dev_log)
        except ValidationError:
            assert False, 'Can`t be ValidationError'


class TestDeviceUpdateSchema:
    @pytest.mark.parametrize(
        'created_at',
        (arrow.now(), )
    )
    def test_pass_not_allowed_keys(self, app, device_uuid, created_at):
        dev_log = {
            'device_uuid': device_uuid,
            'created_at': created_at
        }
        try:
            with app.app_context():
                DeviceLogUpdateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'created_at' in e.messages

    def test_partial_update(self, app):
        dev_log = {
            'log': {
                'test': 'msg'
            },
        }
        try:
            with app.app_context():
                DeviceLogUpdateSchema.load(dev_log)
        except ValidationError:
            assert False, 'Can`t be ValidationError'


class TestDevicesReadSchema:
    def test_read(self, app):
        with app.app_context():
            dev_logs = DeviceLog.query.all()
            try:
                DeviceLogReadSchema.dump(dev_logs)
            except ValidationError:
                assert False, 'Can`t be ValidationError'
