
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