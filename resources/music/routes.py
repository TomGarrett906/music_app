from flask import request
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required

from resources.artists.ArtistModel import ArtistModel
from . MusicModel import MusicModel
from schemas import MusicSchema
from . import bp



#----------------------------------------------------------------------
@bp.route('/')
class MusicList(MethodView):

    @jwt_required()
    @bp.response(200, MusicSchema(many=True))
    def get(self):
        return MusicModel.query.all()

    @jwt_required()
    @bp.arguments(MusicSchema)
    @bp.response(200, MusicSchema)
    def post(self, music_data):
        jwt = get_jwt_identity()
        user_id = jwt['sub']
        m = MusicModel(**music_data, user_id = user_id)        
        try:        
            m.save()
            return m
        except IntegrityError:
            abort(400, message="Invalid Artist ID")


#----------------------------------------------------------------------
@bp.route('/<music_id>')
class Music(MethodView):

    @jwt_required()
    @bp.response(200, MusicSchema)
    def get(self, music_id):
       m = MusicModel.query.get(music_id) 
       if m:
           return m
       abort(400, message='Invalid Music ID')

    @jwt_required()
    @bp.arguments(MusicSchema) 
    @bp.response(200, MusicSchema)       
    def put(self, music_data, music_id):        
            m = MusicModel.query.get(music_id)
            if m and music_data['body']:
                user_id = get_jwt_identity
                if m.user_id == user_id():
                    m.body = music_data['body']
                    m.save()
                    return m
                else:
                    abort(401, message='Unauthorized')
            abort(400, message="Invalid Music Data")


    @jwt_required()
    def delete(self, music_id):
        user_id = get_jwt_identity()
        m = MusicModel.query.get(music_id)
        if m:
            if m.user_id == user_id:
                m.delete()
                return {'message': 'Post Deleted'}, 202            
            abort(401, message='Artist doesn\'t have rights')
        abort(400, message='Invalid Music ID')