from flask import Flask
import os
import sys
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from flask_cors import CORS

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
from routes import routes
