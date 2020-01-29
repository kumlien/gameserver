
<<<<<<< HEAD
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def m1(self):
        print('hej från server')

    def do_POST(self):
        print('Post...')

    def do_GET(self):
        print('Get called from', self.address_string())
        self.send_response(200, 'hej')
        #self.wfile.write('hej')
        self.end_headers()
=======
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server():
    def m1(self):
        print('hej från server')
>>>>>>> d6d7b74b1a48a54682aa71eb86cfcd462e51176d
