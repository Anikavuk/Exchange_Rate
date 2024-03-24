import json
import sqlite3
import urllib.request
import env
import dto.currencies_DTO
import dao.currencies_DAO
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from dao.currencies_DAO import CurrencyDAO
from loguru import logger



logger.add('errors.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


class CurrenciesController:
    """Класс обработчик запроса"""
    @logger.catch
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        code = parsed_url.path.split('/')[-1]
        if code == 'currencies':
            try:
                response = CurrencyDAO(env.path_to_database).all_currencies()
                logger.debug(response)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except sqlite3.DatabaseError as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))
        if not code:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f"Код валюты {code} отсутствует в адресе".encode('utf-8'))

    @logger.catch
    def do_POST(self):
        if self.path == '/currencies':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_data_dict = dict(urllib.parse.parse_qsl(post_data))

                full_name = post_data_dict.get("name")
                code = post_data_dict.get("code")
                sign = post_data_dict.get("sign")
                if full_name is None or code is None or sign is None:
                    self.send_response(400)
                    self.send_header('Content-Type', "application/json")
                    self.end_headers()
                    self.wfile.write(f"The required form field is missing: name, code, sign".encode('utf-8'))
                    return

                save_response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).save_currency(code, full_name,sign)
                response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
                data = dto.currencies_DTO.CurrencyDTO(response.id, response.full_name, response.code, response.sign)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data.to_dict()).encode('utf-8'))

            except sqlite3.IntegrityError as e:
                self.send_response(409)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'A currency with this code already exists {e}'.encode('utf-8'))

            except sqlite3.DatabaseError as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))


