from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from src.RequestHandler import MyRequestDispatcher

PORT = 8080
ADDRESS = ''

#Entry point. Fire up a http server listening on ADDRESS:PORT
#Let the RequestHandler handle the requests...
def main(server_class=HTTPServer, handler_class=MyRequestDispatcher):
    server_address = (ADDRESS, PORT)
    httpd = server_class(server_address, handler_class)
    print('Up and running on port', PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    main()


