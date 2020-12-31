from marshmallow import Schema, fields, INCLUDE


class List(Schema):
    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE

    id = fields.Int()
    user_id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True, default=None)
    is_private = fields.Bool(default=False)
    links = fields.Str()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime(allow_none=True, default=None)


class ListsPagination(Schema):
    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE

    total = fields.Int()
    to = fields.Int()
    from_num = fields.Int(data_key="from")
    prev_page_url = fields.Str(allow_none=True, default=None)
    prev_page = fields.Str()
    per_page = fields.Str()
    path = fields.Str()
    next_page_url = fields.Str(allow_none=True, default=None)
    last_page_url = fields.Str()
    last_page = fields.Int()
    first_page_url = fields.Str()

    data = fields.List(fields.Nested(List))
    current_page = fields.Int()
