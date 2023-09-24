from marshmallow import Schema, fields

class LocationSchema(Schema):
    class Meta:
        fields = ('lat', 'long', 'type')
        ordered = True

class UploadsSchema(Schema):
    location = fields.Nested(LocationSchema)

    class Meta:
        fields = ('id', 'state', 'location', 'user_id')

