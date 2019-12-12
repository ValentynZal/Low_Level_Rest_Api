import socket


URLS = {
    '/users': 'user list',
    '/users/create' : 'create user',
    '/users/user/id': 'user detail',
}

def parse_request(request):
    ''' returns method and url '''
    parsed = request.split(' ')
    return (parsed[0], parsed[1])

def gen_headers(method, url):
    ''' returns headers and code'''
    if not method == 'GET':
        return('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS.keys():
        return('HTTP/1.1 404 Method not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)

def gen_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'

    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'

    return f'<h1>{URLS[url]}</h1>'


def gen_response(request):
    method, url = parse_request(request)
    # print(f'method: {method} url: {url}')
    headers, code = gen_headers(method, url)
    # print(f'headers: {headers} code: {code}')
    body = gen_content(code, url)
    # print(f'body: {body}')
    return (headers + body).encode()

def run():
    ''' create and setup both server and client sockets, handle requests '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request.decode('utf-8').split(' '))
        # print(request.decode('utf-8'), '\n')
        # print(request)
        print()
        # print(addr)

        response = gen_response(request.decode('utf-8'))
        print(response)

        client_socket.sendall(response)
        client_socket.close()

if __name__ == '__main__':
    run()

