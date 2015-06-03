from datetime import datetime, timedelta
from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from peak.util.proxies import ObjectProxy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qxI7M2u3dLYXUxn4eS1c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/gol.db'

auth = ObjectProxy(HTTPBasicAuth())
db = ObjectProxy(SQLAlchemy(app))
board = ObjectProxy(None)
redis_client = ObjectProxy(None)

last_board_update = datetime.now() - timedelta(seconds=2)  # is immediately stale


import game_of_life_web_server.view