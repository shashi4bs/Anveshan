from app import anveshan_user_db
from db import User

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

    status['status'] = 'OK'
    status['code'] = 200
    status['message'] = "Success"
    return status