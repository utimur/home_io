__all__ = [
    'get_scripts',
    'create_script',
    'get_script',
    'update_script',
    'delete_script'
]


from flask import request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import bindparam

from . import parser
from .. import api
from ..responses.script import *
from ..schemas import ScriptUpdateSchema, ScriptsReadSchema, ScriptCreateSchema
from ..schemas.utils import update_instance
from ..view_decorators import json_mimetype_required
from ...common.responses import PaginateResponse
from ...common.schemas import PaginationSchema
from ....models import db, Script


@api.route('/scripts', methods=['GET'])
@jwt_required
@parser.use_kwargs(PaginationSchema, locations=('query',))
def get_scripts(page, per_page):
    bq = Script.baked_query + (
        lambda q: q.filter(Script.owner_id == bindparam('owner_id'))
    )
    bq_params = {
        'owner_id': current_user.id
    }

    return PaginateResponse(
        bq,
        ScriptsReadSchema,
        page,
        per_page,
        bq_params
    )


@api.route('/scripts', methods=['POST'])
@jwt_required
@json_mimetype_required
@parser.use_kwargs(ScriptCreateSchema, locations=('json',))
def create_script(name, tag, code):
    # TODO: celery task
    # TODO:
    #   - save script as file
    #   - run async task
    #   - return success response
    pass


@api.route('/scripts/<int:s_id>', methods=['GET'])
@jwt_required
def get_script(s_id):
    script = Script.query.get(s_id)
    if script is None:
        return ScriptNotFoundResponse()
    if script.owner_id != current_user.id:
        return ScriptAccessDeniedResponse()
    return ScriptResponse(script)


@api.route('/scripts/<int:s_id>', methods=['PATCH'])
@jwt_required
def update_script(s_id):
    script = Script.query.get(s_id)
    if script.owner_id != current_user.id:
        return ScriptAccessDeniedResponse()
    update_instance(ScriptUpdateSchema, script, request.json)
    db.session.commit()
    return ScriptResponse(script)


@api.route('/scripts/<int:s_id>', methods=['DELETE'])
@jwt_required
def delete_script(s_id):
    script = Script.query.get(s_id)
    if script.owner_id != current_user.id:
        return ScriptAccessDeniedResponse()
    db.session.remove(script)
    db.session.commit()
    return ScriptDeleteResponse(script)
