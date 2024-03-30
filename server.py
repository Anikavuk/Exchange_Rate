import json
import urllib
import urllib.parse
from decimal import Decimal
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from loguru import logger

import router.router
from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController
from controller.rate_controller import RateController
from controller.rates_controller import RatesController
from service.service import ServiceExchange

logger.add('server.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


class Server(BaseHTTPRequestHandler):

    def send_error_response(self, error_response):
        error_code = list(error_response.keys())[0]
        error_message = error_response[error_code]
        self.send_response(error_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(error_message.encode('utf-8'))

    @logger.catch
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split('/')[1]
        if path in router.router.routes:
            handler_class = router.router.routes[path]
            if isinstance(handler_class(), (RatesController, CurrenciesController)):
                response = handler_class.do_GET(self)
            if isinstance(handler_class(), (RateController, CurrencyController)):
                code = parsed_url.path.split('/')[-1]
                response = handler_class.do_GET(self, code)
            if isinstance(handler_class(), ServiceExchange):
                query = parsed_url.query
                query_params = parse_qs(query)
                from_currency = query_params['from'][0]
                to_currency = query_params['to'][0]
                amount = float(Decimal(query_params['amount'][0]))
                response = handler_class.do_GET(self, from_currency, to_currency, amount)
        if len(response) == 1:
            self.send_error_response(response)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

    @logger.catch
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data_dict = dict(urllib.parse.parse_qsl(post_data))

        if self.path == '/exchangeRates':
            rates_obj = CurrenciesController()
            response = rates_obj.do_POST(post_data_dict)
        if self.path == '/currencies':
            currencies_obj = CurrenciesController()
            response = currencies_obj.do_POST(post_data_dict)


        if len(response) == 1:
            self.send_error_response(response)
        else:
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PATCH(self):
        parsed_url = urllib.urlparse(self.path)
        path = parsed_url.path

        if path in router.router.routes:
            handler = router.router.routes[path]()
            handler.handle_request('PATCH')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

# a = Server()
# a
