from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from src.RequestHandler import MyRequestDispatcher
import logging

PORT = 8080
ADDRESS = ''

#Entry point. Fire up a http server listening on ADDRESS:PORT
#Let the RequestHandler handle the requests...
def main(server_class=HTTPServer, handler_class=MyRequestDispatcher):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(threadName)s %(asctime)s %(message)s',
                    handlers=[logging.FileHandler("game_server.log"),
                              logging.StreamHandler()])
    server_address = (ADDRESS, PORT)
    httpd = server_class(server_address, handler_class)
    logging.info('Up and running on port %s', str(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Shutting down...\n')


if __name__ == "__main__":
    main()


