import json
import sqlite3
import urllib.request
from http.client import HTTPException

import dao.rates_DAO
import env

from urllib.parse import urlencode

from loguru import logger

from controller.base_controller import BaseController
from error_response import ErrorResponse

logger.add('rate_errors.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class RateController(BaseController):
    """Класс обработчик запроса GET/exchangeRate/USDRUB
    PATCH http://localhost:8080/exchangeRate/EURRUB
    """
    @logger.catch
    def do_GET(self, code):
        """
        Метод получения конкретного обменного курса
        """
        try:
            if len(code) == 6:
                response = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(code)
                logger.error(response)
                return response
            else:
                return ErrorResponse.error_response(exception=HTTPException())
        except IndexError:
            return ErrorResponse.error_response(exception=IndexError())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=sqlite3.DatabaseError())

    def do_PATCH(self):
        parsed_url = urllib.parse.urlparse(self.path)
        code = parsed_url.path.split('/')[-1]
        if len(code) == 6:
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_data_dict = dict(urllib.parse.parse_qsl(post_data))

                rate = post_data_dict.get("rate")
                if rate is None:
                    self.send_response(400)
                    self.send_header('Content-Type', "application/json")
                    self.end_headers()
                    self.wfile.write(f"The required form field is missing: rate".encode('utf-8'))
                    return

                save_response = dao.rates_DAO.ExchangeDAO(env.path_to_database).update_rate(code[:3],
                                                                                            code[3:],
                                                                                            rate)
                response = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(code)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except IndexError:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'The currency pair is missing from the database'.encode('utf-8'))

            except sqlite3.DatabaseError as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))
