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
