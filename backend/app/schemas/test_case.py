from marshmallow import fields
from ..extensions import ma

class TestCaseVersionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    version = fields.Int()
    name = fields.Str()
    release_ready = fields.Bool()

class TestCaseSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    versions = fields.List(fields.Nested(TestCaseVersionSchema))
