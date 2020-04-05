from app import anveshan_user_db
from db import User
from utils.resource_utils import allocate_resource_for_user

def register_user(user):
    status = {}
    #check if password == confirm_password
    if user['password'] != user['confirm_password']:
        status['status'] = 'ERROR'
        status['code'] = 403
        status['message'] = 'password and confirm_password should be similar'
        return status

    #check if user ailready present
    u = User.query.filter(User.username==user['username']).first()
    if u:
        status['status'] = 'ERROR'
        status['code'] = 403
        status['message'] = "Already exists"
        return status

    #make new user
    new_user = User()
    new_user.username = user['username']
    new_user.password = user['password']
    new_user.save()
        
    allocate_resource_for_user(new_user)
    status['status'] = 'OK'
    status['code'] = 200
    status['message'] = "Success"
    return status

def validate_user(user_info):
    status = {}
    #search if user exists
    user = User.query.filter(User.username==user_info['username'], User.password == user_info['password']).first()
    #if user exists with given credentials
    if user:
        status['status'] = 'OK'
        status['code'] = 200
        status['message'] = 'Success'
        return status, user

    #invalid credentials
    status['status'] = 'ERROR'
    status['code'] = 401
    status['message'] = 'Invalid Username or Password'
    return status, None

    
