from flask_jwt_extended import jwt_required

from . import parser
from .. import api
from ..responses.user import *
from ..schemas import UserCreateSchema
from ..view_decorators import json_mimetype_required
from ....models import User, db


@api.route('/users', methods=['POST'])
@json_mimetype_required
@parser.use_kwargs(UserCreateSchema, locations=('json',))
def create_new_user(email, username, password):
    user = User.query.filter(
        User.username == username
    ).one_or_none()
    if user is not None:
        return UsernameAlreadyExistsResponse()
    user = User.query.filter(
        User.email == email
    ).one_or_none()
    if user is not None:
        return EmailAlreadyExistsResponse()

    user = User(
        email=email,
        username=username,
        password=password,
    )
    db.session.add(user)
    db.session.commit()
    return UserResponse(user)


@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    user = User.query.filter(
        User.id == user_id
    ).one_or_none()
    if user is None:
        UserNotFoundResponse()
    return UserResponse(user)


# @api.route('/users/<int:id>', methods=['PATCH'])
# @json_mimetype_required
# @use_kwargs(UserCreateSchema,locations=('json',))
# def update_user(id):
#     pass