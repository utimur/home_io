from uuid import uuid4

import pytest
from sqlalchemy import bindparam

from ...models import User
from ...models.device import Device


@pytest.fixture(scope='function')
def device_uuid(app, db):
    with app.app_context():
        u = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(u)
        db.session.flush()

        # create device to read
        d = Device(
            uuid=uuid4(),
            name='testdevice',
            owner_id=u.id
        )
        u.devices.append(d)
        db.session.commit()
        return d.uuid


class TestDevice:
    @pytest.mark.parametrize(
        'name',
        ('testdevice', 'device')
    )
    def test_create(self, app, db, name):
        with app.app_context():
            u = User(
                username='testuser',
                email='testuser@mail.com',
                password='TestPassword'
            )
            db.session.add(u)
            db.session.flush()

            d = Device(
                uuid=uuid4(),
                name=name,
            )
            u.devices.append(d)
            db.session.commit()

    def test_read(self, app, db, device_uuid):
        with app.app_context():
            # try to read device
            bq = Device.baked_query + (lambda q: q
                .filter(Device.uuid == bindparam('device_uuid'))
            )
            bq_params = {
                'device_uuid': device_uuid
            }
            d = (bq(db.session())
                .params(bq_params)
                .one_or_none())
            assert d is not None

    @pytest.mark.parametrize(
        'name',
        ('newname',)
    )
    def test_update(self, app, db, name, device_uuid):
        with app.app_context():
            # read user
            bq = Device.baked_query + (lambda q: q
                .filter(Device.uuid == bindparam('device_uuid'))
            )
            bq_params = {
                'device_uuid': device_uuid
            }
            d = (bq(app.db.session())
                .params(bq_params)
                .one_or_none())

            # update device data
            d.name = name
            db.session.add(d)
            db.session.commit()

    def test_delete(self, app, db, device_uuid):
        with app.app_context():
            # read device
            bq = Device.baked_query + (lambda q: q
                .filter(Device.uuid == bindparam('device_uuid'))
            )
            bq_params = {
                'device_uuid': device_uuid
            }
            d = (bq(db.session())
                .params(bq_params)
                .one_or_none())

            # delete device
            db.session.delete(d)
            db.session.commit()
