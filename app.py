from flask import Flask
import os
import sys
from flask_mongoalchemy import MongoAlchemy

sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler/AnveshanCrawler"))

sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler"))

from constants import MONGODB_LINK
app = Flask(__name__)
app.config["MONGOALCHEMY_DATABASE"] = "AnveshanUser"
anveshan_user_db =  MongoAlchemy(app)
from routes import routes
