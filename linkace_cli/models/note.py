from marshmallow import Schema, fields


class Note(Schema):
    id = fields.Int()
    user_id = fields.Int()
    link_id = fields.Int()
    note = fields.Str()
    is_private = fields.Bool(default=False)

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime(allow_none=True, default=None)
