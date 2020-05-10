from app import app, login_manager
import os
from search import Search
import json
from bson import Binary
from flask import request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from utils.user_utils import register_user, validate_user
from utils.resource_utils import load_user_resource, get_tag_from_content, update_weights
from utils.query_utils import log_query
from db import User
import traceback
from query import Query
from utils.async_utils import run_in_parallel
from crawlers.crawl import get_pages

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
        #add query to log
        query = Query(query)
        print(query)
        results = anveshan.search(query)
        #[print(res['url'], ' ', res['title']) for res in results]
        urls = []
        response = []
        [(response.append({'_id': str(res['_id']), 'url': res['url'], 'title': res['title']}), urls.append(res['url'])) for res in results if res['url'] not in urls]
        response = {"search_results": response}
        #log_query(query)
        run_in_parallel(log_query, query)
        run_in_parallel(get_pages, response["search_results"], query)
        if query.do_you_mean:
                response["do_you_mean"] = query.true_query
        return json.dumps(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {"search_results": "No result Found"}
        if query.do_you_mean:
                response["do_you_mean"] = query.true_query
        return json.dumps(response)

@app.route('/<user>/search/<query>', methods=['GET'])
@login_required
def personalized_search(user, query):
    print(user, query)
    user = current_user
    try:
        query = Query(query)
        results = anveshan.personalized_search(query, user_resources[user.username])
        urls = []        
        response = []
        [(response.append({'_id': str(res['_id']), 'url': res['url'], 'title': res['title']}), urls.append(res['url'])) for res in results if res['url'] not in urls]
        
        response = {"search_results": response}
        run_in_parallel(log_query, query, user.username)
        run_in_parallel(log_query, query)
        run_in_parallel(get_pages, response["search_results"], query)
        if query.do_you_mean:
                response["do_you_mean"] = query.true_query
        return json.dumps(response)

    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {"search_results": "No result Found"}
        if query.do_you_mean:
                response["do_you_mean"] = query.true_query
        return json.dumps(response)

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


@app.route('/update_bias', methods=['POST'])
@login_required
def update_bias():
    global user_resources
    user = current_user
    _id = request.json['_id']
    tags = get_tag_from_content(_id)
    print(user_resources.keys())
    #update_weights(anveshan.graph.graph, tags, user, user_resources[user.username], anveshan.graph.links)
    run_in_parallel(update_weights, anveshan.graph.graph, tags, user, user_resources[user.username], anveshan.graph.links)
    status = {
        'status' : 'OK',
        'code' : 200,
        'message' : "Success"
    }
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

