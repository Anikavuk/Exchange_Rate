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

loguru.logger.add('../service.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class ServiceExchange(http.server.BaseHTTPRequestHandler):
    """Класс обработчик запроса GET http://localhost:8080/exchange?from=EUR&to=RUB&amount=10"""

    @loguru.logger.catch
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if 'from' in query_params and 'to' in query_params and 'amount' in query_params:
            from_currency = query_params['from'][0]
            to_currency = query_params['to'][0]
            amount = float(Decimal(query_params['amount'][0]))
            try:
                response = dao.rates_DAO.ExchangeDAO(env.path_to_database).getting_specific_exchange_rate(
                    from_currency + to_currency)
                rate = float(response['rate'])
            except IndexError:
                try:
                    response = dao.rates_DAO.ExchangeDAO(env.path_to_database).getting_specific_exchange_rate(
                        to_currency + from_currency)
                    rate = float(1 / Decimal(response['rate']))
                except IndexError:
                    currency_USD = 'USD'
                    response_from = dao.rates_DAO.ExchangeDAO(env.path_to_database).getting_specific_exchange_rate(
                        currency_USD + from_currency)
                    response_to = dao.rates_DAO.ExchangeDAO(env.path_to_database).getting_specific_exchange_rate(
                        currency_USD + to_currency)
                    rate = round(float(Decimal(response_to['rate']) / Decimal(response_from['rate'])), 6)
                    response = {'baseCurrency': response_from['targetCurrency'],
                                'targetCurrency': response_to['targetCurrency'], 'rate': rate}

            data = dto.service_DTO.ServiceDTO(response['baseCurrency'],
                                              response['targetCurrency'],
                                              round(rate, 6),
                                              amount,
                                              round(float(rate * amount), 6))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data.to_dict()).encode('utf-8'))


# host = "localhost"
# port = 8080
# server = http.server.HTTPServer((host, port), ServiceExchange)
# server.serve_forever()
