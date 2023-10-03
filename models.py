from marshmallow import Schema, fields
# from models.submodule import ExtractDataSchema


class ExtractDataSchema(Schema):
    pdf = fields.Field(required=True)

    # pdf = fields.Str()