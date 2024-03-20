import http.server
from server import Server

server = http.server.HTTPServer(('localhost', 8080), Server)

if __name__ == '__main__':
    server.serve_forever()

# host = "localhost" '127.0.0.1'
# port = 8080
# server = http.server.HTTPServer((host, port), Server)
# server.serve_forever()
