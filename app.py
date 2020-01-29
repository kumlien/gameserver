<<<<<<< HEAD
from http.server import HTTPServer
from src.HttpServer import RequestHandler

def main():
    server = HTTPServer(("0.0.0.0", 8080), RequestHandler)
    server.serve_forever()
=======
from src.HttpServer import Server

def main():
    server = Server()
    server.m1()
>>>>>>> d6d7b74b1a48a54682aa71eb86cfcd462e51176d

if __name__ == "__main__":
    main()


