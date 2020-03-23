from app import app, login_manager
import os
from search import Search
import json
from flask import request
from flask_login import login_user, login_required, logout_user, current_user
from utils.user_utils import register_user, validate_user
from db import User

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

@app.route('/login', methods=['POST'])
def login():
    user = {
        "username": request.json['username'],
        "password": request.json['password'],
        "remember_me": request.json['remember_me']
    }
    remember_me = user['remember_me']
    
    status, user = validate_user(user)
    if status['code'] == 200:
        #session['username'] = user.username 
        login_user(user, remember=remember_me)

    return status

@login_manager.user_loader
def load_user(username):
    return User.query.filter(User.username == username).first()

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    #session.pop('username', None)
    user = current_user
    print(user)
    user.authenticated = False
    logout_user()
    status = {}
    status['status'] = "OK"
    status['code'] = 200
    status['message'] = "Success"
    return status
    
@login_manager.unauthorized_handler
def unauthorized():
    status = {}
    status['status'] = "ERROR"
    status['code'] = 401
    status['message'] = "Anauthorized"
    return status
