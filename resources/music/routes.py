from flask import request
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort

from schemas import MusicSchema
from . import bp
from database import music


#----------------------------------------------------------------------
@bp.route('/')
class MusicList(MethodView):
    def get(self):
        return {'music': music}

    @bp.arguments(MusicSchema)
    def post(self, music_data):
        music[uuid4().hex] = music_data
        return music_data, 201


#----------------------------------------------------------------------
@bp.route('/<music_id>')
class Music(MethodView):
    def get(self, music_id):
        try:
            mu = music[music_id]
            return mu, 200
        except KeyError:
            abort(404, message="music not found")

    @bp.arguments(MusicSchema)        
    def put(self, music_data,music_id):
        if music_id in music:
            mu = music[music_id]
            if music_data['artist_id'] != music['artist_id']:
                abort(400, message= "Not able to edit another artist's music")
            mu['body'] = music_data['body']
            return mu, 200
        abort(404, message="music not found")

    def delete(self, music_id):
        try:
            deleted_music = music.pop(music_id)
            return {'message':f"{deleted_music['body']} deleted"}, 202
        except:
            abort(404, message="music not found")