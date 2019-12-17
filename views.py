import json
from bson.json_util import dumps
from init_db import users


def user_list(): 
    ''' retrieve users '''
    # pull users from db
    req_users = users.find()
    # return users as json
    context = {
        'count': 0,
        'results': []
    }
    for user in req_users:
        context['count'] = context.get('count') + 1
        context['results'].append(user)

    # print(context)

    return json.dumps(context) 


def user_create(req_body, user_id = []): 
    ''' create user '''
    # modify id
    if not user_id:
        id_dict = {"_id": 1}
        print(id_dict)
        user_id.append(2)
    else:
        idx = len(user_id)-1  
        id_dict = {"_id": user_id[idx]}
        print(id_dict)
        user_id.append(user_id[idx]+1)

    # parse request body
    new_user = json.loads(req_body)
    # print(new_user)

    # append new_user dict to id_dict
    id_dict.update(new_user)

    # push user into db
    users.insert_one(id_dict)

    user_created = users.find_one(id_dict)

    return json.dumps(user_created)
    


def user_detail(user_id, method, req_body):
    ''' retrieve, delete, update user '''
    print()
    print(user_id, method, req_body)

    query = {"_id": int(user_id)}
    print(query)

    if method == 'GET':
        user = users.find_one(query)
        # print(user)

        return json.dumps(user)    

    if method == 'DELETE':
        users.delete_one(query) 
        return json.dumps({'message': 'user is successfully deleted'})  

    if method == 'PUT':
        new_values = json.loads(req_body)
        print(new_values)
        users.update_one(query, {"$set":new_values})
        return json.dumps({'message': 'user data is successfully updated'}) # return updated user

    # if there is no user with such id -> 404 {"user": "Not found"}
    
