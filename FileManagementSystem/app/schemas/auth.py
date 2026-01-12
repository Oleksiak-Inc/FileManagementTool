from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class TokenSchema(Schema):
    access_token = fields.Str()
