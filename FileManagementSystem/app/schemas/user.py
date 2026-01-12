from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    user_type_id = fields.Int()


class UserCreateSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    user_type_id = fields.Int(load_default=None)
