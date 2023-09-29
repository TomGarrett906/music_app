from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)

database = SQLAlchemy(app)
migrate = Migrate(app, database)
api = Api(app)
jwt = JWTManager(app)

from resources.artists import bp as artist_bp
api.register_blueprint(artist_bp)
from resources.music import bp as music_bp
api.register_blueprint(music_bp)

from resources.artists import routes
from resources.music import routes
from resources.artists.ArtistModel import ArtistModel
from resources.music.MusicModel import MusicModel
