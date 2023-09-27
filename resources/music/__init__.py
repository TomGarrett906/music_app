from flask_smorest import Blueprint

bp = Blueprint('music', __name__, url_prefix='/music', description='Ops on music')

from . import routes
from . import MusicModel