from flask import Flask
import os
import sys
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO

sys.path.append(os.path.abspath("/home/vipul/Desktop/SE/Anveshan_Crawler/AnveshanCrawler"))

sys.path.append(os.path.abspath("/home/vipul/Desktop/SE/Anveshan_Crawler"))

from constants import MONGODB_LINK
app = Flask(__name__)
app.secret_key = "secret"
app.config["MONGOALCHEMY_DATABASE"] = "AnveshanUser"

#cors

cors = CORS(app)

login_manager = LoginManager(app)
anveshan_user_db =  MongoAlchemy(app)

#socketio
socketio = SocketIO(app, cors_allowed_origins="*")


from routes import routes, socket_routes

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port=5000)
	#app.run()
