from app import app
import os

from search import Search
import json

anveshan = Search()

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/search/<query>')
def search(query):
    results = anveshan.search(query)
    [print(res['url'], ' ', res['title']) for res in results]
    response = []
    [response.append({'url': res['url'], 'title': res['title']}) for res in results]
    return json.dumps(response)
