import ast

from marshmallow import fields, validate, Schema, ValidationError
from marshmallow_arrow import ArrowField

from ....models import Script


class ScriptSchema(Schema):
    model = Script

    id = fields.Integer()

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=64),
            validate.Regexp(r'(^|,)[\w]+(,|$)', 0)
        ]
    )

    tag = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=64),
            validate.Regexp(r'(^|,)[\w]+(,|$)', 0)
        ]
    )

    @staticmethod
    def validate_code(code):
        try:
            ast.parse(code)
        except SyntaxError:
            raise ValidationError('Not a valid Python code.')

    code = fields.Raw(
        required=True,
        validate=[
            validate.Length(min=0, max=2048),
            lambda code: ScriptSchema.validate_code(code)
        ]
    )

    calls = fields.Integer()

    runtime = fields.Integer()

    created_at = ArrowField()

    updated_at = ArrowField()

    owner_id = fields.Nested(
        'UserSchema',
        many=False
    )
