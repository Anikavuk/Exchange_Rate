import json
import sqlite3

import dao.currencies_DAO
import env
import dto.currencies_DTO
from loguru import logger


logger.add('my_errors.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class CurrencyController:
    """Класс обработчик запроса GET http://localhost:8080/currency/USD"""
    @logger.catch
    def do_GET(self, code):
        """
        Метод получения конкретной валюты
        """
        if len(code) == 3:
            try:
                response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
                data = dto.currencies_DTO.CurrencyDTO(response.id, response.full_name, response.code, response.sign)
                logger.error(data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data.to_dict()).encode('utf-8'))
            except IndexError:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f"Валюта не найдена: {code}".encode('utf-8'))
                return
            except sqlite3.DatabaseError as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f"Код валюты {code} отсутствует в адресе".encode('utf-8'))
