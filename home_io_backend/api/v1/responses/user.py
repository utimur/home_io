from ..schemas import UserReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'UserResponse',
    'UserNotFoundResponse',
    'UserInvalidPasswordResponse',
    'UsernameAlreadyExistsResponse',
    'EmailAlreadyExistsResponse'
]


class UserResponse(JsonApiResponse):
    def __init__(self, user):
        super().__init__(UserReadSchema.dump(user), 200)


class UserNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('USER_NOT_FOUND', 404)


class UserInvalidPasswordResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('USER_INVALID_PASSWORD', 400)


class UsernameAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('USERNAME_ALREADY_EXISTS', 400)


class EmailAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('EMAIL_ALREADY_EXISTS', 400)
