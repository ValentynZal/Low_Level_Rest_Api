import json
from init_db import users


def user_list(): 
    # TODO:  
    # pull users from db
    # return users as json
    return json.dumps({'users': 'users'})


def user_create(req_body):   
    # TODO: 
    # accept json 
    # push user into db
    return json.dumps({'message': 'new user is created'})
    


def user_detail(id, method, req_body):
    # TODO: 
    # pull user with corresponding id from db
    # return json
    return json.dumps({'user_id': id})
