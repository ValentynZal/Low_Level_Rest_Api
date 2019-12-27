import json
import re
from bson.json_util import dumps
from init_db import users, db


user_id_list = [1]


def user_list(): 
    ''' retrieve users '''
    # pull users from db
    req_users = users.find()
    # return users as json
    context = []
    for user in req_users:
        context.append(user)

    print(context)

    return json.dumps(context) 

def user_create(req_body): 
    ''' create user '''
    # autoincrement id
    global user_id_list
    # id_dict = {}

    idx = len(user_id_list)-1  
    id_dict = {"_id": user_id_list[idx]}
    user_id_list.append(user_id_list[idx]+1)

    # parse request body
    new_user = json.loads(req_body)
    # print(new_user)

    # append new_user dict to id_dict
    id_dict.update(new_user)

    # push user into db
    users.insert_one(id_dict) # inserted_id

    user_created = users.find_one(id_dict)

    return json.dumps(user_created)
    


def user_detail(user_id, method, req_body):
    ''' retrieve, delete, update user '''
    global user_id_list

    print()
    print(user_id, method, req_body)

    query = {"_id": int(user_id)}
    print(query)

    user = users.find_one(query)
    # print(user)
    if not user:
        return None

    if method == 'GET':
        
        return json.dumps(user)    

    if method == 'DELETE':
        global user_id_list
        users.delete_one(query) 
        user_id_list.remove(int(user_id)) # remove id
        return json.dumps({'message': f'user with id:{user_id} is successfully deleted'})  

    if method == 'PUT':
        new_values = json.loads(req_body)
        print(new_values)
        users.update_one(query, {"$set":new_values})
        return json.dumps(users.find_one(query)) 

    # if there is no user with such id -> 404 {"user": "Not found"}
    
