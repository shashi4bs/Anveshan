from flask import Flask
import os
import sys
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager

sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler/AnveshanCrawler"))

sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler"))

from constants import MONGODB_LINK
app = Flask(__name__)
app.secret_key = "secret"
app.config["MONGOALCHEMY_DATABASE"] = "AnveshanUser"

login_manager = LoginManager(app)
anveshan_user_db =  MongoAlchemy(app)
from routes import routes
