import pytest


def pytest_make_parametrize_id(config, val):
    return repr(val)


@pytest.fixture(scope='module')
def app():
    from .. import app
    return app


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        app.db.drop_all()
        app.db.create_all()
    return app.db
