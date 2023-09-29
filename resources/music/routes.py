from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from resources.artists.ArtistModel import ArtistModel
from .MusicModel import MusicModel
from schemas import MusicSchema
from . import bp



#----------------------------------------------------------------------
@bp.route('/')
class MusicList(MethodView):
    @bp.response(200, MusicSchema(many=True))
    def get(self):
        return MusicModel.query.all()

    @bp.arguments(MusicSchema)
    def post(self, music_data):
        m = MusicModel(**music_data)
        a = ArtistModel.query.get(music_data['artist_id'])
        if a:
            m.save()
            return m
        else:
            abort(400, message="Invalid Artist ID")


#----------------------------------------------------------------------
@bp.route('/<music_id>')
class Music(MethodView):
    @bp.response(200, MusicSchema)
    def get(self, music_id):
       m = MusicModel.query.get(music_id) 
       if m:
           return m
       abort(400, message='Invalid Music ID')

    @bp.arguments(MusicSchema) 
    @bp.response(200, MusicSchema)       
    def put(self, music_data, music_id):        
            m = MusicModel.query.get(music_id)
            if m and music_data['body']:
                if m.music_id == music_data['music_id']:
                    m.body = music_data['body']
                    m.save()
                    return m
            abort(400, message="Invalid Music Data")


    def delete(self, music_id):
        req_data = request.get_json()
        artist_id = req_data['artist_id']
        m = MusicModel.query.get(music_id)
        if m:
            if m.artist_id == artist_id:

                m.delete()
                return {'message': 'Post Deleted'}, 202
            
            abort(400, message='Artist doesn\'t have rights')
        abort(400, message='Invalid Music ID')