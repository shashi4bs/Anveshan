from flask import Flask
import os
import sys
sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler/AnveshanCrawler"))

sys.path.append(os.path.abspath("/home/shashi/Desktop/SE/Anveshan/AnveshanCrawler"))

app = Flask(__name__)

from routes import routes
