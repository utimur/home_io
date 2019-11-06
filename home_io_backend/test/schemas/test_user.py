import pytest
from marshmallow.exceptions import ValidationError

from ...api.v1.schemas import UserReadSchema, UsersReadSchema, \
    UserCreateSchema, UserUpdateSchema
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


class TestUserReadSchema:
    def test_read(self, app, user):
        with app.app_context():
            user = User.query.all()[0]
            try:
                res = UserReadSchema.dump(user)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestUserCreateSchema:
    @pytest.mark.parametrize(
        'username, email, password',
        (('test', 'mail@mail.com', 'TestPassword'),
         ('12345', 'mail@mail.com', 'TestPassword'),
         ('very_long_username_very_long_username_very_long', 'mail@mail.com', 'TestPassword'),
         ('@@@@@#####----', 'mail@mail.com', 'TestPassword'),)
    )
    def test_invalid_username(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        try:
            UserCreateSchema.load(user_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'username' in e.messages

    @pytest.mark.parametrize(
        'username, email, password',
        (('testuser', 'test', 'TestPassword'),
         ('testuser', '@mail.com', 'TestPassword'),
         ('testuser', 'very_long_email_very_long_email' * 2 + '@mail.com', 'TestPassword'),
         ('testuser', '@###$$$$@mail.com', 'TestPassword'),)
    )
    def test_invalid_email(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        try:
            UserCreateSchema.load(user_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'email' in e.messages

    @pytest.mark.parametrize(
        'username, email, password',
        (('testuser', 'mail@mail.com', 'test'),
         ('testuser', 'mail@mail.com', 'very_long_password_very_long_password_very_long'),
         ('testuser', 'mail@mail.com', '@!@#!@#!@#!#!'),)
    )
    def test_invalid_password(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        try:
            UserCreateSchema.load(user_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'password' in e.messages

    @pytest.mark.parametrize(
        'user_id, username, email, password, created_at',
        ((1, 'testuser', 'mail@mail.com', 'TestPassword', 'ANYTIME'), )
    )
    def test_pass_not_allowed_keys(self, user_id, username, email, password, created_at):
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'password': password,
            'created_at': created_at
        }
        try:
            UserCreateSchema.load(user_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'username, email, password',
        (('testuser', 'mail@mail.com', 'TestPassword'), )
    )
    def test_valid_data(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        try:
            UserCreateSchema.load(user_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'


class TestUserUpdateSchema:
    @pytest.mark.parametrize(
        'user_id, created_at',
        ((1, 'ANYTIME'), )
    )
    def test_pass_not_allowed_keys(self, user_id, created_at):
        user_data = {
            'id': user_id,
            'created_at': created_at
        }
        try:
            UserUpdateSchema.load(user_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'username, email, password',
        (('testuser', 'mail@mail.com', 'TestPassword'), )
    )
    def test_partial_update(self, username, email, password):
        user_data = {
            'username': username,
        }
        try:
            UserUpdateSchema.load(user_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'


class TestUsersReadSchema:
    def test_read(self, app, user):
        with app.app_context():
            users = User.query.all()
            try:
                res = UsersReadSchema.dump(users)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'
