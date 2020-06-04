from app import app, login_manager
import os
from search import Search
import json
from bson import Binary
from flask import request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from utils.user_utils import register_user, validate_user
from utils.resource_utils import load_user_resource, update_weight
from utils.query_utils import log_query
from db import User, UserContributions
import traceback
from query import Query
from utils.async_utils import run_in_parallel, run_process, test
from crawlers.crawl import get_pages, crawl_pages
from parallel import kill_thread
from flask_request_validator import Param, Pattern, validate_params


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
        run_process(test, 1, 2, 3)
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

@app.route('/<user>/search', methods=['POST'])
@login_required
def personalized_search(user):
    query = request.json['query']
    personalization = request.json['personalization']

    user = current_user
    print(user.pr_inconsistent, user.pr_updated)
    if user.pr_inconsistent and user.pr_updated:
        user_resources[user.username] = load_user_resource(current_user)
        user.pr_inconsistent=False
        user.save() 
    try:
        query = Query(query)
        results = anveshan.personalized_search(query, user_resources[user.username], personalization=personalization)
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
    print(user, status)
    if status['code'] == 200:
        #session['username'] = user.username 
        login_user(user, remember=remember_me)
        #load user resource #graph for user
        resource = load_user_resource(current_user)
        user_resources[current_user.username] = resource

    return status

@app.route('/update_weights', methods=['POST'])
@login_required
def update_weights():
    bm25 = request.json['bm25']
    pr = request.json['pr']
    status = {}
    if bm25 <= 0 and pr <= 0:
        status['status'] = "ERROR"
        status['code'] = 422
        status['message'] = 'Unprocessable Entity'
        return status
    user = current_user
    user.bm25 = bm25
    user.pr = pr
    user.save()
    status['status'] = "OK"
    status['code'] = 200
    status['messgae'] = "Success Weights Updated"
    return status
   
@app.route('/details', methods=['GET'])
@login_required
def user_details():
    user = current_user
    tags = user.tags
    if len(tags)>5:
        tag = tag[:5]
    return json.dumps(
        {
            'tags' : user.tags,
            'bm25' : user.bm25,
            'pr' : user.pr
        }
    )

@app.route('/set_tag', methods=['POST'])
@login_required
def set_tags():
    tags = request.json["tags"]
    user = current_user
    if type(tags) == list:
        user.tags = tags
        user.save()
        status = {
            "status" : "OK",
            "code" : 200,
            "message" : "Tags Updated"
        }
        return status
    else:
        status = {
            "status" : "ERROR",
            "code" : 422,
            "message" : "Invalid Tag"
        }

@app.route('/update_bias', methods=['POST'])
@login_required
def update_bias():
    global user_resources
    user = current_user
    _id = request.json['_id']
    print(user_resources.keys())
    #update_weight(_id, user.username)
    user.pr_inconsistent = True
    user.pr_updated = False
    user.save()
    print(user.pr_inconsistent, user.pr_updated, user.username)
    run_in_parallel(update_weight, _id, user.username)
    status = {
        'status' : 'OK',
        'code' : 200,
        'message' : "Success"
    }
    return status

@app.route('/contribute', methods=['POST'])
def contribute():
    url = request.json["url"]
    tags = request.json["tags"]
    description = request.json["description"]
    user = current_user
    try:
        contribution = UserContributions.query.filter(UserContributions.url == url).first()
        print(contribution)
        if not contribution:
            contribution = UserContributions()
            contribution.tags = tags
            contribution.description = description
            contribution.url = url.encode()
            contribution.save()
        #crawl_pages(url, user.username)
        status = {
            "status" : "OK",
            "code" : 200,
            "message" : "Page Added"
        }
    except Exception as e:
        print(e)
        status = {
            "status" : "ERROR",
            "code" : 422,
            "message" : "Unprocessable Entity"
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
    
@app.route('/delete', methods=['GET'])
@login_required
def delete_account():
    user = current_user
    #delete user resources
    #todo 
    '''
        delete user resources
        delete user entry
    '''
    status = {}
    status['status'] = "OK"
    status['code'] = 200
    status['message'] = 'Success Account Deleted'
    return status

@login_manager.unauthorized_handler
def unauthorized():
    status = {}
    status['status'] = "ERROR"
    status['code'] = 401
    status['message'] = "Anauthorized"
    return status

@app.after_request
def after(res):
    #r = json.loads(res.get_data())
    #if current_user.is_authenticated:
    #    print(session)
    #    #r['s_id'] = session['_id']
    #res.set_data(json.dumps(r))
    return res
