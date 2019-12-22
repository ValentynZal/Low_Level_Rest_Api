'''
Here we are testing path from request for predenting in URLS,
as well as for alloewd methods.
'''
import requests
import json


url2 = 'http://127.0.0.1:5000/users/create'
payload = {
    "name":"val",
    "surname":"zal",
    "birth_date":"1994-09-11",
    "gender":"man",
    "profession":"software developer",
    "bio":"I fond of coding" 
}
print(f'Requesting {url2}')
r2 = requests.post(url2, json=payload)
print(f'Response code: {r2.status_code}\n Json Response: {r2.text}\n')
# r3 = requests.post(url2,  data=json.dumps(payload))
# print(f'Response code: {r3.status_code}\n Json Response: {r3.text}\n')
# r4 = requests.post(url2,  data=json.dumps(payload))
# print(f'Response code: {r4.status_code}\n Json Response: {r4.text}\n')


# url = 'http://127.0.0.1:5000/users'
# print(f'Requesting {url}')
# r = requests.get(url)
# print('Response code: ', r.status_code, '\n')

# url3 = 'http://127.0.0.1:5000/users/user/1'
# payload = {'key1':'value1', 'key2':'value2'}
# r3 = requests.put(url3, data=payload)
# print(f'Requesting {url3} to update')
# print('Response code: ', r3.status_code, '\n')

# url4 = 'http://127.0.0.1:5000/users/user/1'
# payload = {'key1':'value1', 'key2':'value2'}
# r4 = requests.delete(url4, data=payload)
# print(f'Requesting {url4} to delete')
# print('Response code: ', r4.status_code, '\n')

# url5 = 'http://127.0.0.1:5000/useers'
# print(f'Requesting {url5}')
# r5 = requests.get(url5)
# print('Response code: ', r5.status_code, '\n')

# url6 = 'http://127.0.0.1:5000/users/user/1'
# payload = {'key1':'value1', 'key2':'value2'}
# r6 = requests.post(url6, data=payload)
# print(f'Requesting {url6}')
# print('Response code: ', r6.status_code, '\n')

# url7 = 'http://127.0.0.1:5000/users'
# payload = {'key1':'value1', 'key2':'value2'}
# r7 = requests.delete(url7, data=payload)
# print(f'Requesting {url7} to delete')
# print('Response code: ', r7.status_code, '\n')