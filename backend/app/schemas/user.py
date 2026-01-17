from marshmallow import fields
from ..extensions import ma

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    active = fields.Bool()

class UserCreateSchema(UserSchema):
    password = fields.Str(required=True, load_only=True)
