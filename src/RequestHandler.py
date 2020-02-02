from http.server import BaseHTTPRequestHandler, HTTPServer
from src.ControllerRegistry import ControllerRegistry
import re
import logging
from urllib import parse

'''
    Basic request dispatcher
    Dispatches http requests to the configured controllers
    based on the request path.
    Only support GET and POST for now
'''

class MyRequestDispatcher(BaseHTTPRequestHandler):
    registry = ControllerRegistry()

    def do_POST(self):
        logging.info('POST called for %s', self.path)
        parsed_url = parse.urlparse(self.path)
        (resource, id) = self.extractResourceAndId(parsed_url.path)
        handler = MyRequestDispatcher.registry.getController(resource)
        logging.info('Got a handler: %s' + str(handler.__class__))
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        
        (code, headers, body) = handler.handlePost(id, post_data, parse.parse_qs(parsed_url.query))
        self.sendResponse(code, headers, body)

    def do_GET(self):
        (resource, id) = self.extractResourceAndId(self.path)
        logging.info('GET called for %s', resource)
        handler = MyRequestDispatcher.registry.getController(resource)
        logging.info('Dispatching to handler of type %s', handler.__class__)
        if id is None:
            (code, headers, body) = handler.handleGet()
        else:   
            (code, headers, body) = handler.handleGet(id)
        self.sendResponse(code, headers, body)
    
        
    def sendResponse(self, code, headers, body):
        logging.info('Sending back %s %s %s ', code, headers, body)
        self.send_response(code)
        for header in headers.items():
            self.send_header(header[0], header[1])
        self.end_headers()
        if(body is not None):
            self.wfile.write(body.encode('utf8'))


    # todo handle more than one '/' in path, like '//'
    def extractResourceAndId(self, path):
        logging.info('Extracting resource and possibly id from path %s', path)
        resource = ''
        id = None
        if path[0]=='/':
            path=path[1:]
        
        if len(path) > 1 and path[len(path)-1]=='/':
            path=path[0:len(path)-2]

        elements = re.split(r'/', path)
        if elements is not None and len(elements) > 0:
            id = elements[0]
        if len(elements) > 1:
            resource = elements[1]
        logging.info('Extracted resource: %s and id: %s', resource, id)
        return resource, id