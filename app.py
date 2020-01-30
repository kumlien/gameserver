from http.server import HTTPServer
from src.HttpServer import RequestHandler

def main():
    server = HTTPServer(("0.0.0.0", 8080), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()


