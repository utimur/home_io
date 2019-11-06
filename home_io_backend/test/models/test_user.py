import pytest
from sqlalchemy import bindparam

from ...models import User


@pytest.fixture(scope='function')
def user(app, db):
    with app.app_context():
        # create user to read
        u = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(u)
        db.session.commit()
        return u


class TestUser:
    @pytest.mark.parametrize(
        'username, email, password',
        (('testuser', 'testuser@mail.com', 'TestPassword'),
        ('home_io_user', 'home_io_user@mail.com', 'sEcReTpAsSwOrD'))
    )
    def test_create(self, app, db, username, email, password):
        with app.app_context():
            u = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(u)
            db.session.commit()

    @pytest.mark.usefixtures('user')
    def test_read(self, app, db):
        with app.app_context():
            # try to read user
            bq = User.baked_query + (lambda q: q
                .filter(User.id == bindparam('user_id'))
            )
            bq_params = {
                'user_id': 1
            }
            u = (bq(db.session())
                .params(bq_params)
                .one_or_none())
            assert u is not None

    @pytest.mark.parametrize(
        'username, email, password',
        (('newname', 'newemail@mail.com', 'NewPassword'),)
    )
    @pytest.mark.usefixtures('user')
    def test_update(self, app, db, username, email, password):
        with app.app_context():
            # read user
            bq = User.baked_query + (lambda q: q
                .filter(User.id == bindparam('user_id'))
            )
            bq_params = {
                'user_id': 1
            }
            u = (bq(app.db.session())
                .params(bq_params)
                .one_or_none())

            # update user data
            u.username = username
            u.email = email
            u.password = password
            db.session.add(u)
            db.session.commit()

    @pytest.mark.usefixtures('user')
    def test_delete(self, app, db):
        with app.app_context():
            # read user
            bq = User.baked_query + (lambda q: q
                .filter(User.id == bindparam('user_id'))
            )
            bq_params = {
                'user_id': 1
            }
            u = (bq(db.session())
                .params(bq_params)
                .one_or_none())

            # delete user
            db.session.delete(u)
            db.session.commit()
