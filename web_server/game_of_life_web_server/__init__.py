from datetime import datetime, timedelta
from flask import Flask
from peak.util.proxies import ObjectProxy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qxI7M2u3dLYXUxn4eS1c'

board = ObjectProxy(None)
tick_period = ObjectProxy(None)
redis_client = ObjectProxy(None)

last_board_update = datetime.now() - timedelta(seconds=2)  # is immediately stale


import game_of_life_web_server.view
