from marshmallow import Schema, fields, INCLUDE

from linkace_cli import models


class Link(Schema):
    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE

    id = fields.Int()
    user_id = fields.Int()
    url = fields.Str(allow_none=True)
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


class LinksPagination(Schema):
    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE

    total = fields.Int()
    to = fields.Int()
    from_num = fields.Int(data_key="from")
    prev_page_url = fields.Str(allow_none=True, default=None)
    prev_page = fields.Str()
    per_page = fields.Int()
    path = fields.Str()
    next_page_url = fields.Str(allow_none=True, default=None)
    last_page_url = fields.Str()
    last_page = fields.Int()
    first_page_url = fields.Str()

    data = fields.List(fields.Nested(Link))
    current_page = fields.Int()
