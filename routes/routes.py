from app import app
import os
from search import Search
import json
from flask import request
from user_utils.utils import register_user

anveshan = Search(generate_pr_score=False)

@app.route('/')
@app.route('/home')
def home():
    return "Anveshan"

@app.route('/search/<query>', methods=['GET'])
def search(query):
    try:
        results = anveshan.search(query)
        #[print(res['url'], ' ', res['title']) for res in results]
        response = []
        [response.append({'url': res['url'], 'title': res['title']}) for res in results]
        return json.dumps(response)
    except Exception as e:
        print(e)
        return json.dumps("No result Found")

@app.route('/register', methods=['POST'])
def register():
    user = {
        "username": request.json['username'],
        "password": request.json['password'],
        "confirm_password": request.json['confirm_password'],
    }
    
    #status = {status: str, status_code: int, message: str}
    status = register_user(user)
    return status
