
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_smorest import abort
from f
from schemas import ArtistSchema, AuthArtistSchema
from sqlalchemy.exc import IntegrityError
from . import bp
from .ArtistModel import ArtistModel


@bp.post('/register')
@bp.arguments(ArtistSchema)
@bp.response(201, ArtistSchema)       
def register(artist_data):
        artist = ArtistModel()
        artist.from_dict(artist_data)
        try:
            artist.save()
            return artist_data
        except IntegrityError:
            abort(400, message='This Username or Email is taken')    


@bp.post('/login')
@bp.arguments(AuthArtistSchema)
def login(login_info):
    if 'username' not in login_info and 'email' not in login_info:
        abort(400, message='Plese include Username or Email')
    if 'username' in login_info:
        artist = ArtistModel.query.filter_by(username=login_info['user_name']).first()
    else:
        artist = ArtistModel.query.filter_by(email=login_info['user_name']).first()
    if artist and artist.check_password(login_info['password']):
        access_token = create_access_token(indentity=artist.id)
        return {'access_token': access_token}
    abort(400, message='Invalid Usernaem or password')
             
     
@bp.route('/logout')

