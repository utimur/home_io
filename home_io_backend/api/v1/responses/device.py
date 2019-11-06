from ..schemas import DeviceReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'DeviceResponse',
    'DeviceNotFoundResponse',
    'DeviceAlreadyExistResponse',
]


class DeviceResponse(JsonApiResponse):
    def __init__(self, device):
        super().__init__(DeviceReadSchema.dump(device), 200)


class DeviceNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('deviceNotFound', 404)


class DeviceAlreadyExistResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('deviceAlreadyExist', 400)

