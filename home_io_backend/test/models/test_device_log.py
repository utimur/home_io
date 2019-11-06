import uuid

import pytest
from sqlalchemy import bindparam

from ...models import DeviceLog, Device, User


@pytest.fixture(scope='function')
def device_log_id(app, db):
    with app.app_context():
        user = User(
            username='username',
            email='afsfkask@mail.ru',
            password='password'
        )

        db.session.add(user)
        db.session.flush()

        device = Device(
            uuid=uuid.uuid4(),
            name='device_name'
        )

        user.devices.append(device)
        db.session.flush()

        device_log = DeviceLog(
            log={'name': 'log1'}
        )
        device.device_logs.append(device_log)
        db.session.commit()
        return device_log.id


class TestDeviceLog:

    def test_create(self, app, db):
        with app.app_context():
            user = User(
                username='username',
                email='afsfkask@mail.ru',
                password='password'
            )

            db.session.add(user)
            db.session.flush()

            device = Device(
                uuid=uuid.uuid4(),
                name='device_name'
            )

            user.devices.append(device)
            db.session.flush()

            device_log = DeviceLog(
                log={'name': 'log1'}
            )
            device.device_logs.append(device_log)
            db.session.commit()

    @pytest.mark.usefixtures('device_log_id')
    def test_read(self, app, db, device_log_id):
        with app.app_context():
            bq = DeviceLog.baked_query + (lambda q: q
                .filter(DeviceLog.id == bindparam('device_log_id'))
            )
            bq_params = {
                'device_log_id': device_log_id
            }

            device_log = (bq(app.db.session())
                          .params(bq_params)
                          .one_or_none())
            assert device_log is not None

    @pytest.mark.usefixtures('device_log_id')
    def test_update(self, app, db, device_log_id):
        with app.app_context():
            bq = DeviceLog.baked_query + (lambda q: q
                                          .filter(DeviceLog.id == bindparam('device_log_id')))
            bq_params = {
                'device_log_id': device_log_id
            }

            device_log = (bq(app.db.session())
                          .params(bq_params)
                          .one_or_none())
            device_log.log = {
                'log': 'newlog'
            }
            db.session.add(device_log)
            db.session.commit()

    @pytest.mark.usefixtures('device_log_id')
    def test_delete(self, app, db, device_log_id):
        with app.app_context():
            bq = DeviceLog.baked_query + (lambda q: q
                                          .filter(DeviceLog.id == bindparam('device_log_id')))
            bq_params = {
                'device_log_id': device_log_id
            }

            device_log = (bq(app.db.session())
                          .params(bq_params)
                          .one_or_none())
            db.session.delete(device_log)
            db.session.commit()
