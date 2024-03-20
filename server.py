import urllib
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import urllib.parse
import router.router
import controller.currency_controller


class BaseHandler(SimpleHTTPRequestHandler):

    def handle_request(self, method):
        if method == 'GET':
            self.do_GET()
        elif method == 'POST':
            self.do_POST()
        elif method == 'PATCH':
            self.do_PATCH()
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f"Валюта не найдена".encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Response from GET')

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Response from POST')

    def do_PATCH(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Response from PATCH')

class Server(BaseHandler):

    def do_GET(self):
        parsed_url = urllib.urlparse(self.path)
        path = parsed_url.path

        if path in router.router.routes:
            handler = router.router.routes[path]()
            handler.handle_request('GET')
        if path in router.router.routes:
            handler = router.router.routes[path]()
            handler.handle_request('POST')
        if path in router.router.routes:
            handler = router.router.routes[path]()
            handler.handle_request('PATCH')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')
