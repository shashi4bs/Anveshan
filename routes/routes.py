from app import app, login_manager
import os
from search import Search
import json
from flask import request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from utils.user_utils import register_user, validate_user
from utils.resource_utils import load_user_resource
from db import User

anveshan = Search(generate_pr_score=False)

user_resources = dict()

@app.route('/')
@app.route('/home')
def home():
    return "Anveshan"

@app.route('/search/<query>', methods=['GET'])
def search(query):
    if current_user.is_authenticated:
        redirect("/{}/search/{}".format(current_user.username, query))
    try:
        results = anveshan.search(query)
        #[print(res['url'], ' ', res['title']) for res in results]
        response = []
        [response.append({'url': res['url'], 'title': res['title']}) for res in results]
        return json.dumps(response)
    except Exception as e:
        print(e)
        return json.dumps("No result Found")

@app.route('/<user>/search/<query>', methods=['GET'])
@login_required
def personalised_search(user, query):
    print(user, query)
    user = current_user
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
    global user_resources
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
        #load user resource #graph for user
        resource = load_user_resource(current_user)
        user_resources[current_user.username] = resource

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
    #clean user resource
    del user_resources[current_user.username]
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

