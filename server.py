import urllib
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from controller.currency_controller import CurrencyController


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path_name = parsed_url.path.split('/')[-1]
        if path_name == 'currencies':
            self.CurrenciesController.do_GET()
        if len(path_name) == 3:
            currency_controller = CurrencyController()
            currency_controller.do_GET(path_name)
        # if path_name == 'exchangeRates':
        #     self.RatesController.do_GET()
        # if len(path_name) == 6:
        #     self.RateController.do_GET()
        # if path_name == 'exchange':
        #     self.ServiceExchange.do_GET()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()