import uuid

import pytest
from marshmallow.exceptions import ValidationError

from ...api.v1.schemas import DeviceReadSchema, DevicesReadSchema, \
    DeviceCreateSchema, DeviceUpdateSchema
from ...models import Device, User


@pytest.fixture(scope='function')
def device(app, db):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(user)
        db.session.flush()

        device = Device(
            uuid=uuid.uuid4(),
            name='testdevice',
            owner_id=user.id
        )
        db.session.add(device)
        db.session.commit()
        return device


class TestDeviceReadSchema:
    def test_read(self, app, device):
        with app.app_context():
            device = Device.query.all()[0]
            try:
                res = DeviceReadSchema.dump(device)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceCreateSchema:
    @pytest.mark.parametrize(
        'name',
        ('tet',
         'very_long_devname_very_long_devname_very_long',
         '@@@@@#####----')
    )
    def test_invalid_device(self, name):
        device_data = {
            'name': name
        }
        try:
            DeviceCreateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'name' in e.messages

    @pytest.mark.parametrize(
        'name',
        ('test_device',)
    )
    def test_valid_data(self, name):
        device_data = {
            'name': name,
        }
        try:
            DeviceCreateSchema.load(device_data)
        except ValidationError:
            assert False, 'Can`t be ValidationError'

    @pytest.mark.parametrize(
        'dev_uuid, name, owner_id, registered_at',
        ((uuid.uuid4(), 'test_device', 1, 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, dev_uuid, name, owner_id, registered_at):
        device_data = {
            'uuid': uuid,
            'name': name,
            'owner_id': owner_id,
            'registered_at': registered_at
        }
        try:
            DeviceCreateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'registered_at' in e.messages
            assert 'owner_id' in e.messages


class TestDeviceUpdateSchema:
    @pytest.mark.parametrize(
        'dev_uuid, registered_at',
        ((uuid.uuid4(), 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, dev_uuid, registered_at):
        device_data = {
            'uuid': dev_uuid,
            'registered_at': registered_at
        }
        try:
            DeviceUpdateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'uuid' in e.messages
            assert 'registered_at' in e.messages

    @pytest.mark.parametrize(
        'name',
        ('test_device',)
    )
    def test_partial_update(self, name):
        device_data = {
            'name': name
        }
        try:
            DeviceUpdateSchema.load(device_data)
        except ValidationError:
            assert False, 'Can`t be ValidationError'


class TestDevicesReadSchema:
    def test_read(self, app, device):
        with app.app_context():
            devices = Device.query.all()
            try:
                DevicesReadSchema.dump(devices)
            except ValidationError:
                assert False, 'Can`t be ValidationError'
