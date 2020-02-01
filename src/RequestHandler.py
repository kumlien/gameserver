from http.server import BaseHTTPRequestHandler, HTTPServer
from src.ControllerRegistry import ControllerRegistry
import re

'''
    Very complex request dispatcher... 
    Dispatches http requests to the configured controllers
    based on the request path.
    Only support GET and POST for now
'''

class MyRequestDispatcher(BaseHTTPRequestHandler):
    registry = ControllerRegistry()

    def do_POST(self):
        print('POST called for', self.path)
        handler = MyRequestDispatcher.registry.getController(self.path)
        print('Got a handler:', handler.__name__)


    def do_GET(self):
        resource = self.extractResource(self.path)
        print('GET called for ', resource)
        handler = MyRequestDispatcher.registry.getController(resource)
        print('Got a handler:', handler.__class__)
        (code, headers, body) = handler.handleGet()
        print('Got ', code, headers, body, 'from controller')
        self.send_response(code, body)
        for header in headers.items():
            self.send_header(header[0], header[1])
        self.wfile.write(body.encode('utf8'))
        


    # We only handle one level deep paths like 'users', not 'api/users'
    def extractResource(self, path):
        print('Extract resource part from path', path)
        resource = ''
        if path[0]=='/':
            path=path[1:]

        elements = re.split(r'/', path);
        if elements is not None and len(elements) > 0:
            resource = elements[0]
        print('Extracted resource', resource)
        return resource