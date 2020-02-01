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
        (resource, id) = self.extractResourceAndId(self.path)
        print('GET called for ', resource)
        handler = MyRequestDispatcher.registry.getController(resource)
        print('Got a handler:', handler.__class__)
        if id is None:
            (code, headers, body) = handler.handleGet()
        else:   
            (code, headers, body) = handler.handleGet(id)
        print('Got ', code, headers, body, 'from controller')
        self.send_response(code, body)
        for header in headers.items():
            self.send_header(header[0], header[1])
        self.end_headers()
        self.wfile.write(body.encode('utf8'))
    
        


    # We only handle one level deep paths like 'users', not 'api/users'
    def extractResourceAndId(self, path):
        print('Extract resource part from path', path)
        resource = ''
        id = None
        if path[0]=='/':
            path=path[1:]

        elements = re.split(r'/', path);
        if elements is not None and len(elements) > 0:
            resource = elements[0]
        if len(elements) > 1:
            id = elements[1]
        print('Extracted resource', resource)
        return resource, id