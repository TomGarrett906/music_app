from flask_smorest import Blueprint

bp = Blueprint('artists', __name__, description='Ops on Artists')

from . import routes