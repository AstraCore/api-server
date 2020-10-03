from flask_socketio import SocketIO
from flask_caching import Cache
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
from server import config
import eventlet
import time

eventlet.monkey_patch()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = config.secret
cache = Cache(config={"CACHE_TYPE": "simple"})
sio = SocketIO(app, cors_allowed_origins="*", async_mode = "eventlet", message_queue = "redis://")
cache.init_app(app)
CORS(app)

start_time = time.monotonic()
socket_counter = 0
rest_counter = 0

watch_addresses = {}
subscribers = {}
connections = 0
thread = None
mempool = []

from server import esplora
from server import routes
from server import socket
from server import rest

esplora.init(app)
routes.init(app)
socket.init(sio)
rest.init(app)
