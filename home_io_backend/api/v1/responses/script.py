__all__ = [
    'ScriptResponse',
    'ScriptDeleteResponse',
    'ScriptNotFoundResponse',
    'ScriptAccessDeniedResponse'
]

from ..schemas import ScriptReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse


class ScriptResponse(JsonApiResponse):
    def __init__(self, script):
        super().__init__(ScriptReadSchema.dump(script), 200)


class ScriptResponse(JsonApiResponse):
    def __init__(self, script):
        super().__init__(ScriptReadSchema.dump(script), 200)


class ScriptDeleteResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('', 200)


class ScriptAccessDeniedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_ACCESS_DENIED', 403)


class ScriptNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_NOT_FOUND', 404)
