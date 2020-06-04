from flask import Flask
import os
import sys
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO

#import eventlet
#eventlet.monkey_patch()

sys.path.append(os.path.abspath("/home/shashi/Desktop/Anveshan_FYP/SE/Anveshan_Crawler/AnveshanCrawler"))

sys.path.append(os.path.abspath("/home/shashi/Desktop/Anveshan_FYP/SE/Anveshan_Crawler"))
sys.path.append(os.path.abspath("/home/shashi/Desktop/Anveshan_FYP/SE/Anveshan"))

from constants import MONGODB_LINK
app = Flask(__name__)
app.secret_key = "secret"
app.config["MONGOALCHEMY_DATABASE"] = "AnveshanUser"
app.config.update({
'SESSION_COOKIE_SECURE': True,
'REMEMBER_COOKIE_SECURE' : True
})
#cors

cors = CORS(app, origin="*")

login_manager = LoginManager(app)
anveshan_user_db =  MongoAlchemy(app)

#socketio
#socketio = SocketIO(app, cors_allowed_origins="*",)
socketio = SocketIO()
app.config['SESSION_TYPE'] = 'filesystem'
socketio.init_app(app, cors_allowed_origins="*", message_queue="redis://")


from routes import routes, socket_routes

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port=5001)
	#app.run()
