from marshmallow import Schema, fields

class ExtractDataSchema(Schema):
    pdf = fields.Field(required=True)

    # pdf = fields.Str()