from ...common.responses import JsonApiResponse


__all__ = [
    'LoginResponse',
]


class LoginResponse(JsonApiResponse):
    def __init__(self, token):
        response = {
            'access_token': token
        }
        super().__init__(response, 200)
