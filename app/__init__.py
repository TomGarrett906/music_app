from flask import Flask
from flask_smorest import Api
from Config import Config
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

from resources.artists import bp as artist_bp
api.register_blueprint(artist_bp)
from resources.music import bp as music_bp
api.register_blueprint(music_bp)

from resources.artists import routes
from resources.music import routes
