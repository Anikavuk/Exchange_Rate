import json
import sqlite3
import urllib.request
from urllib.parse import parse_qs

from loguru import logger

import dao.rates_DAO
import env
from controller.base_controller import BaseController

logger.add('rates_controller.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


class RatesController(BaseController):
    """Класс - обработчик запроса
    GET http://localhost:8080/exchangeRates
    POST http://localhost:8080/exchangeRates"""

    @logger.catch
    def do_GET(self):
        response = dao.rates_DAO.ExchangeDAO(env.path_to_database).all_exchange_rates()
        logger.debug(response)
        return response
        # except sqlite3.DatabaseError as e:
        #     self.send_response(500)
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))
        # except Exception:
        #     self.send_response(400)
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(f"Запрос не верен".encode('utf-8'))

    @logger.catch
    def do_POST(self):
        # if self.path == '/exchangeRates':
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data_dict = dict(urllib.parse.parse_qsl(post_data))

            baseCurrency = post_data_dict.get("baseCurrencyCode")
            targetCurrency = post_data_dict.get("targetCurrencyCode")
            rate = post_data_dict.get("rate")
            if baseCurrency is None or targetCurrency is None or rate is None:
                self.send_response(400)
                self.send_header('Content-Type', "application/json")
                self.end_headers()
                self.wfile.write(
                    f"The required form field is missing: baseCurrencyCode, targetCurrencyCode, rate".encode('utf-8'))
                return

            save_rate = dao.rates_DAO.ExchangeDAO(env.path_to_database).save_rate(baseCurrency, targetCurrency, rate)
            if save_rate is None:
                self.send_response(409)
                self.send_header('Content-Type', "application/json")
                self.end_headers()
                self.wfile.write(f"A currency pair with this code already exists".encode('utf-8'))
                return
            response = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
                baseCurrency + targetCurrency)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except IndexError:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                f'One (or both) currency from the currency pair does not exist in the database'.encode('utf-8'))

        except sqlite3.DatabaseError as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))
