from marshmallow import Schema, fields

class MusicSchema(Schema):
    id = fields.Str(dumps_only = True)
    body = fields.Str(required = True)
    user_id = fields.Str(required = True)

class ArtistSchema(Schema):
    id = fields.Str(dumps_only = True)
    username = fields.Str(required = True)
    email = fields.Str(required = True)
    password = fields.Str(required = True)
    first_name = fields.Str()
    last_name = fields.Str()

class UpdateArtistSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required = True)
    new_password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
