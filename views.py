import json
import re
from bson.json_util import dumps
from init_db import users, db


user_id_list = [1]


def user_list(): 
    ''' retrieve users '''

    req_users = users.find()    # pull users from db

    context = [] 
    for user in req_users:
        context.append(user)

    # print(context)

    return json.dumps(context) # return users as json

def user_create(req_body): 
    ''' create user '''
    # autoincrement id
    global user_id_list

    idx = len(user_id_list)-1  
    id_dict = {"_id": user_id_list[idx]}
    user_id_list.append(user_id_list[idx]+1)

    new_user = json.loads(req_body) # parse request body
    id_dict.update(new_user) # appends corresponding id to new user 
    users.insert_one(id_dict) # push user into db

    user_created = users.find_one(id_dict)

    return json.dumps(user_created) # return created user
    


def user_detail(user_id, method, req_body):
    ''' retrieve, delete, update user '''

    global user_id_list

    # print(user_id, method, req_body)
    query = {"_id": int(user_id)}
    user = users.find_one(query)

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

    
