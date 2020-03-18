from app import app
import os

from search import Search
import json

anveshan = Search(generate_pr_score=False)

@app.route('/')
@app.route('/home')
def home():
    return "Anveshan"

@app.route('/search/<query>')
def search(query):
    results = anveshan.search(query)
    #[print(res['url'], ' ', res['title']) for res in results]
    response = []
    [response.append({'url': res['url'], 'title': res['title']}) for res in results]
    return json.dumps(response)
 
    #try:
    #    results = anveshan.search(query)
    #    #[print(res['url'], ' ', res['title']) for res in results]
    #    response = []
    #    [response.append({'url': res['url'], 'title': res['title']}) for res in results]
    #    return json.dumps(response)
    #except Exception as e:
    #    print(e)
    #    return json.dumps("No result Found")
