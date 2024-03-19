import http.server
import json
import urllib.parse
import urllib.request
from decimal import *
from urllib.parse import parse_qs

import loguru

import dao.rates_DAO
import dto.service_DTO
import env
from dao.currencies_DAO import CurrencyDAO

loguru.logger.add('../service.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class ServiceExchange(http.server.BaseHTTPRequestHandler):
    """Класс обработчик запроса GET http://localhost:8080/exchange?from=EUR&to=RUB&amount=10"""
    @staticmethod
    def find_rate(from_currency, to_currency):
        value = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            from_currency + to_currency)
        if value:
            return value['rate']
        if not value:
            value = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
                to_currency + from_currency)
            if value:
                return 1 / value['rate']
        value1 = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            'USD' + from_currency)
        value2 = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            'USD' + to_currency)
        if not value1 or not value2:
            raise IndexError
        cross_rate = value2['rate'] / value1['rate']
        return cross_rate

    @loguru.logger.catch
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if 'from' not in query_params or 'to' not in query_params or 'amount' not in query_params:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f"message: Валюта не найдена".encode('utf-8'))
        else:
            from_currency = query_params['from'][0]
            to_currency = query_params['to'][0]
            amount = float(Decimal(query_params['amount'][0]))

            rate = self.find_rate(from_currency, to_currency)

            data = dto.service_DTO.ServiceDTO(CurrencyDAO(env.path_to_database).find_by_code(from_currency).__dict__,
                                              CurrencyDAO(env.path_to_database).find_by_code(to_currency).__dict__,
                                              round(rate, 6),
                                              amount,
                                              round(float(rate * amount), 6))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data.to_dict()).encode('utf-8'))



host = "localhost"
port = 8080
server = http.server.HTTPServer((host, port), ServiceExchange)
server.serve_forever()




