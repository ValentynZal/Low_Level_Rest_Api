import socket
import re
import json
from init_db import users
from views import user_list, user_create, user_detail


URLS = {
    '/users': user_list,                # GET
    '/users/create' : user_create,      # POST -> pass body to the root
    r'/users/user/\d+': user_detail,    # GET, UPDATE, DELETE -> pass id(all), and body(update)
}


def parse_request(request):
    ''' returns method and url '''

    parsed = request.split(' ')
    return (parsed[0], parsed[1])


def parse_request_body(request):
    return request.split('\r\n\r\n')[1]


def check_404(url):
    ''' check request url in routes'''

    if url not in URLS.keys() and re.match(r'/users/user/\d+', url) is None:
        return True       

    return False


def check_405(method, url):
    ''' check routes for allowed methods'''
           
    if url == '/users':
        if method != 'GET':
            return True
    elif  url == '/users/create':
        if method not in ['GET', 'POST']:
            return True
    else:
        if method not in ['GET', 'PUT', 'DELETE']:
            return True        

    return False


def check_422(req_body):
    user_data = json.loads(req_body)

    headers_422 = 'HTTP/1.1 422 Unprocessable Entity\n\n'
    invalid_len = json.dumps({'message': 'Invalid field length'})  #'<h1>422</h1><p>Invalid field length</p>'
    invalid_date = json.dumps({'message': 'Invalid date format'}) #'<h1>422</h1><p>Invalid date format</p>'
    invalid_select = json.dumps({'message': 'Unexisting select'}) #'<h1>422</h1><p>Unexisting select</p>'


    def valid_len(field_name, length):
        if len(user_data.get(field_name)) > length:
            return False

    def valid_select(field_name, sel=['male', 'female']):
        if user_data.get(field_name) not in sel:
            return False

    def valid_date(field_name, pattern=r'\d{4}-\d{2}-\d{2}'):
        if re.match(pattern, user_data.get(field_name)) == None:
            return False

    for k, v in user_data.items():
        if k in ['name', 'surname', 'profession']:
            check = valid_len(k, 15)
            body = invalid_len
        elif k == 'bio':
            check = valid_len(k, 1024)
            body = invalid_len
        elif k == 'birthdate':
            check = valid_date(k)
            body = invalid_date
        # TODO: not working - check!
        elif k == 'gender':
            check = valid_select(k)
            body = invalid_select

        if check == False:
            return headers_422 + body
        

def gen_headers(method, url):
    ''' returns headers '''

    if check_404(url):
        return('HTTP/1.1 404 Method not found\n\n', 404)
    elif check_405(method, url):
        return('HTTP/1.1 405 Method not allowed\n\n', 405)
    else:    
        return ('HTTP/1.1 200 OK\n\n', 200)
     

def gen_content(code, url, method, req_body=None):
    if code == 404:
        return  json.dumps({'message': 'Page not found'}) #'<h1>404</h1><p>Not found</p>'

    if code == 405:
        return json.dumps({'message': 'Method not allowed'}) # '<h1>405</h1><p>Method not allowed</p>'

    if url == '/users':
        return URLS[url]()        
    elif  url == '/users/create':
        return URLS[url](req_body)        
    else:
        user_id = url.split('/')[3]
        url = r'/users/user/\d+'
        return URLS[url](user_id, method, req_body)        
    

def gen_response(request):
    method, url = parse_request(request)
    # print(f'method: {method} url: {url}')
    headers, code = gen_headers(method, url)
    # print(f'headers: {headers} code: {code}')
    if method == 'POST' or method == 'PUT':
        req_body = parse_request_body(request)
        print(req_body)
        res = check_422(req_body)
        if res != None:
            return res.encode()
    else:
        req_body = None

    res_body = gen_content(code, url, method, req_body)
    
    if res_body == None:
        return ('HTTP/1.1 404 Page is not found\n\n' + json.dumps({'message': 'Page is not found'})).encode()
    # print(f'body: {res_body}')
    return (headers + res_body).encode() # headers.encode()


def run():
    ''' create and setup both server and client sockets, handle requests '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        # print('Connection from', addr)

        request = client_socket.recv(1024)
        # print(request.decode('utf-8').split('r\n\r\n'))
        # print(request.decode('utf-8'))
        print(request)
        
        response = gen_response(request.decode('utf-8'))
        print(response)

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()


