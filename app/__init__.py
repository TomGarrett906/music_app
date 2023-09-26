from flask import Flask

app = Flask(__name__)

from resources.artists import routes
from resources.music import routes