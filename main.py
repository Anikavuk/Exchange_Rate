import http.server

from server import Server

# server = http.server.HTTPServer(('0.0.0.0', 8080), Server)
server = http.server.HTTPServer(('localhost', 8080), Server)

if __name__ == '__main__':
    server.serve_forever()
