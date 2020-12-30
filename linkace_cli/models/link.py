from marshmallow import Schema, fields

from linkace_cli import models


class Link(Schema):
    id = fields.Int()
    user_id = fields.Int()
    url = fields.URL()
    title = fields.Str()
    description = fields.Str(allow_none=True, default=None)
    icon = fields.Str(allow_none=True, default=None)
    is_private = fields.Bool(default=False)
    status = fields.Int()
    check_disabled = fields.Bool(default=False)

    lists = fields.List(fields.Nested(lambda: models.List()))
    tags = fields.List(fields.Nested(lambda: models.Tag()))

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime(allow_none=True, default=None)
