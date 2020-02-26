from app import app
import os
print(os.getcwd())
from search import Search

anveshan = Search()

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/search/<query>')
def search(query):
    results = anveshan.search(query)
    return query
