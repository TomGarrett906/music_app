from flask import request
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort

from schemas import ArtistSchema, UpdateArtistSchema

from . import bp
from database import artists, music


#----------------------------------------------------------------------
@bp.get('/artist')
class ArtistList(MethodView):
    def get(self):
        return {'artists': artists}, 200

    @bp.arguments(ArtistSchema)        
    def post(self, artist_data):
        artists[uuid4().hex] = artist_data
        return artist_data, 201


#----------------------------------------------------------------------
@bp.route('/artist/<artist_id>')
class Artist(MethodView):
    def get(self, artist_id):
        try:
            artist = artists[artist_id]
            return artist, 200
        except KeyError:
            abort(404, message="artist not found")

    @bp.arguments(UpdateArtistSchema)             
    def put(self, artist_data, artist_id):

        try:
            artist = artists[artist_id]
            if artist['password'] != artist_data['password']:
                abort(400, message= 'Incorrect Password')
    
            artist |= artist_data
            if 'new_password' in artist_data:
                new_password = artist.pop("new_password")
                artist['password'] = new_password
            return artist, 200
        except KeyError:
            abort(404, message="artist not found")
  
    def delete(self):
        artist_data = request.get_json()
        for a, artist in enumerate(artists):
            if artist["username"] == artist_data["username"]: artists.pop(a)
        return {"message": f"{artist_data['username']} deleted"}, 202


#----------------------------------------------------------------------
@bp.get('/artist/<artist_id>/music')
def get_artist_music(artist_id):
    if artist_id not in artists:
        abort(404, message="artist not found")
    artist_music = [mu for mu in music.values() if mu['artist_id'] == artist_id]
    return artist_music, 200