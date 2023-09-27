from marshmallow import Schema, fields

class ArtistSchema(Schema):
    id = fields.Str(dumps_only = True)
    username = fields.Str(required = True)
    email = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)
    first_name = fields.Str()
    last_name = fields.Str()

class MusicSchema(Schema):
    id = fields.Str(dumps_only = True)
    body = fields.Str(required = True)
    user_id = fields.Int(required = True)
    timestamp = fields.Str(dump_only=True)
    # artist = fields.List(fields.Nested(ArtistSchema()), dumps_only = True)


class UpdateArtistSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required = True, load_only = True)
    new_password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

class DeleteArtistSchema(Schema):
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)