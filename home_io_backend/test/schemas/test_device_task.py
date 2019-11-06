import uuid

import pytest
from marshmallow.exceptions import ValidationError

from ...api.v1.schemas import DeviceTaskReadSchema, DeviceTaskCreateSchema, DeviceTaskUpdateSchema
from ...models import Device, User, DeviceTask


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
            uuid=uuid.uuid4(),
            name='testdevice',
            owner_id=user.id
        )
        db.session.add(device)
        db.session.commit()
        return device.uuid


@pytest.fixture(scope='function')
def device_task(app, db, device_uuid):
    with app.app_context():
        dev_task = DeviceTask(
            device_uuid=device_uuid,
            task={
                'task': 'task1'
            }
        )
        db.session.add(dev_task)
        db.session.commit()
        return dev_task


class TestDeviceTaskReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()[0]
            try:
                DeviceTaskReadSchema.dump(dev_task)
            except ValidationError:
                assert False, 'Can`t be ValidationError'


class TestDeviceTasksReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()
            try:
                DeviceTaskReadSchema.dump(dev_task)
            except ValidationError:
                assert False, 'Can`t be ValidationError'


class TestDeviceTaskCreateSchema:
    @pytest.mark.parametrize(
        'task',
        (tuple(), )
    )
    def test_invalid_device_task(self, app, task):
        try:
            with app.app_context():
                DeviceTaskCreateSchema.load(task)
                assert False, 'Exception must occur'
        except ValidationError:
            pass

    @pytest.mark.parametrize(
        'task',
        ({'task': 'task'},)
    )
    def test_valid_data(self, app, task, device_uuid):
        try:
            with app.app_context():
                task['device_uuid'] = device_uuid
                DeviceTaskCreateSchema.load(task)
        except ValidationError:
            assert False, 'Can`t be ValidationError'

    @pytest.mark.parametrize(
        'task_id, task, created_at',
        (
            (1, {'task': 'task'}, 'ANYTIME'),
        )
    )
    def test_pass_not_allowed_keys(self, app, task_id, task, created_at, device_uuid):
        device_task_data = {
            'id': task_id,
            'task': task,
            'created_at': created_at,
            'device_uuid': device_uuid,
        }
        try:
            with app.app_context():
                DeviceTaskCreateSchema.load(device_task_data)
                assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages


class TestDeviceTaskUpdateSchema:
    @pytest.mark.parametrize(
        'task_id, created_at',
        ((1, 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, app, task_id, created_at, device_uuid):
        device_task_data = {
            'id': task_id,
            'created_at': created_at,
            'device_uuid': device_uuid
        }
        try:
            with app.app_context():
                DeviceTaskUpdateSchema.load(device_task_data)
                assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'task',
        (({'task': 'task'}, ),)
    )
    def test_partial_update(self, task):
        device_task_data = {
            'task': task,
        }
        try:
            DeviceTaskUpdateSchema.load(device_task_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'
