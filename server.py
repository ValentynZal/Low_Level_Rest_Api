import socket
import re
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
        return False       

    return True



def check_405(method, url):
    ''' check routes for allowed methods'''
           
    if url == '/users':
        if method != 'GET':
            return False
    elif  url == '/users/create':
        if method not in ['GET', 'POST']:
            return False
    else:
        if method not in ['GET', 'PUT', 'DELETE']:
            return False        

    return True


def gen_headers(method, url):
    ''' returns headers '''

    if check_404(url) == False:
        return('HTTP/1.1 404 Method not found\n\n', 404)
    elif check_405(method, url) == False:
        return('HTTP/1.1 405 Method not allowed\n\n', 405)
    else:    
        return ('HTTP/1.1 200 OK\n\n', 200)
     

def gen_content(code, url, method, req_body=None):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'

    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'

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
        res_body = gen_content(code, url, method, req_body)
    else:
        res_body = gen_content(code, url, method)

    if res_body == None:
        return 'HTTP/1.1 404 Page not found\n\n'.encode()

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
        # print()
        # print(request.decode('utf-8'))
        # print()
        print(request)
        
        # print(addr)

        response = gen_response(request.decode('utf-8'))
        print(response)

        client_socket.sendall(response)
        client_socket.close()

if __name__ == '__main__':
    run()


