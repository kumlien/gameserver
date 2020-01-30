from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from src.RequestHandler import RequestHandler

PORT = 8080
ADDRESS = ''

#Entry point. Fire up a http server listening on ADDRESS:PORT
#Let the RequestHandler handle the requests...
def main(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = (ADDRESS, PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    main()


