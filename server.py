import urllib
import urllib.parse
from urllib.parse import urlparse
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler

from loguru import logger

import router.router

logger.add('server.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


# class BaseHandler(SimpleHTTPRequestHandler):
#
#     def handle_request(self, method):
#         if method == 'GET':
#             self.do_GET()
#         elif method == 'POST':
#             self.do_POST()
#         elif method == 'PATCH':
#             self.do_PATCH()
#         else:
#             self.send_response(400)
#             self.send_header('Content-Type', 'application/json')
#             self.end_headers()
#             self.wfile.write(f"Валюта не найдена".encode('utf-8'))
#
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(b'Response from GET')
#
#     # def do_POST(self):
#     #     self.send_response(200)
#     #     self.send_header('Content-type', 'text/html')
#     #     self.end_headers()
#     #     self.wfile.write(b'Response from POST')
#     #
#     # def do_PATCH(self):
#     #     self.send_response(200)
#     #     self.send_header('Content-type', 'text/html')
#     #     self.end_headers()
#     #     self.wfile.write(b'Response from PATCH')


class Server(BaseHTTPRequestHandler):
    @logger.catch
    def do_GET(self):
        parsed_url = urlparse(self.path)
        # path = parsed_url.path.split('/')[-1] # вернет exchangeRates
        path = parsed_url.path # вернет /exchangeRates

        if path in router.router.routes:
            handler = router.router.routes[path]()  #RatesController()
            handler.do_GET()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

    # @logger.catch
    # def do_POST(self):
    #     parsed_url = urllib.urlparse(self.path)
    #     path = parsed_url.path
    #
    #     if path in router.router.routes:
    #         handler = router.router.routes[path]()
    #         handler.handle_request('POST')
    #
    #     else:
    #         self.send_response(404)
    #         self.send_header('Content-type', 'text/html')
    #         self.end_headers()
    #         self.wfile.write(b'Not Found')
    #
    # def do_PATCH(self):
    #     parsed_url = urllib.urlparse(self.path)
    #     path = parsed_url.path
    #
    #     if path in router.router.routes:
    #         handler = router.router.routes[path]()
    #         handler.handle_request('PATCH')
    #     else:
    #         self.send_response(404)
    #         self.send_header('Content-type', 'text/html')
    #         self.end_headers()
    #         self.wfile.write(b'Not Found')
