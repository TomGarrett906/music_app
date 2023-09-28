
from flask.views import MethodView

from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import ArtistSchema, ArtistSchemaNested, UpdateArtistSchema, DeleteArtistSchema

from . import bp
from .ArtistModel import ArtistModel

from database import artists, music


#----------------------------------------------------------------------
@bp.route('/artist')
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

    @bp.arguments(DeleteArtistSchema)  
    def delete(self, artist_data):
        artist = ArtistModel.query.filter_by(username=artist_data['username']).first()
        if artist and artist.check_password(artist_data['password']):
            artist.delete()
            return {"message": f"{artist_data['username']} deleted"}, 202
        abort(400, message="Username or Password Invalid")

#----------------------------------------------------------------------

@bp.route('/artist/<artist_id>')
class Artist(MethodView):
    @bp.response(200, ArtistSchemaNested)       
    def get(self, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id, description='Artist Not Found')
        return artist
    
#UPDATE ARTIST
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



#----------------------------------------------------------------------


@bp.route('/artist/follow.<follower_id>/<followed_id>')
class FollowUser(MethodView):

    @bp.response(200, ArtistSchema(many=True))    
    def post(self, follower_id, followed_id):
        artist = ArtistModel.query.get(follower_id)
        artist_to_follow = ArtistModel.query.get(followed_id)
        if artist and artist_to_follow:
            artist.follow_artist(artist_to_follow)
            return artist.followed.all()
        abort(400, message="artist not found")

    @bp.response(202, ArtistSchema(many=True))    
    def put(self, follower_id, followed_id):
        artist = ArtistModel.query.get(follower_id)
        artist_to_unfollow = ArtistModel.query.get(followed_id)
        if artist and artist_to_unfollow:
            artist.unfollow_artist(artist_to_unfollow)
            return {'message': f'User: {artist_to_unfollow}'}
        abort(400, message="artist not found")