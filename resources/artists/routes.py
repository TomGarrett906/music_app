from flask import request
from flask.views import MethodView

from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import ArtistSchema, UpdateArtistSchema, DeleteArtistSchema

from . import bp
from .ArtistModel import ArtistModel

from database import artists, music


#----------------------------------------------------------------------
@bp.get('/artist')
class ArtistList(MethodView):
    @bp.response(200, ArtistSchema(many = True))
    def get(self):
        artists = ArtistModel.query.all()
        return artists

    @bp.arguments(ArtistSchema)
    @bp.response(201, ArtistSchema)       
    def post(self, artist_data):
        artist = ArtistModel()
        artist.from_dict(artist_data)
        try:
            artist.save()
            return artist_data
        except IntegrityError:
            abort(400, message='This Username or Email is taken')


#----------------------------------------------------------------------
@bp.route('/artist/<artist_id>')
class Artist(MethodView):
    @bp.response(200, ArtistSchema)       
    def get(self, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id, description='Artist Not Found')
        return artist

    @bp.arguments(UpdateArtistSchema)
    @bp.response(202, ArtistSchema)                    
    def put(self, artist_data, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id, description='Artist Not Found')
        if artist and artist.check_password(artist_data['password']):
            try:
                artist.from_dict(artist_data)
                artist.save()
                return artist
            except IntegrityError:
                abort(400, message='This Username or Email is taken')

    @bp.arguments(DeleteArtistSchema)  
    def delete(self, artist_data):
        artist_data = request.get_json()
        artist = ArtistModel.query.filter_by(username=artist_data['username']).first()

        if artist and artist.check_password(artist_data['password']):
            artist.delete()
            return {"message": f"{artist_data['username']} deleted"}, 202
        abort(400, message="Username or Password Invalid")

#----------------------------------------------------------------------
@bp.response(200, ArtistSchema(many=True))       
@bp.get('/artist/<artist_id>/music')
def get_artist_music(artist_id):
    if artist_id not in artists:
        abort(404, message="artist not found")
    artist_music = [mu for mu in music.values() if mu['artist_id'] == artist_id]
    return artist_music