import json
import sqlite3
from http.client import HTTPException

import dao.currencies_DAO
import env
import dto.currencies_DTO
from loguru import logger

from controller.base_controller import BaseController

logger.add('my_errors.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class CurrencyController(BaseController):
    """Класс обработчик запроса http://localhost:8080/currency/USD"""
    @logger.catch
    def do_GET(self, code):
        """
        Метод получения конкретной валюты
        """
        try:
            if len(code) == 3:
                data = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
                response = dto.currencies_DTO.CurrencyDTO(data.id, data.full_name, data.code, data.sign).to_dict()
                logger.error(data)
            if not code:
                response = self.error_response(HTTPException)
        except IndexError:
            response = self.error_response(IndexError)
        except sqlite3.DatabaseError:
            response = self.error_response(sqlite3.DatabaseError)
        return response




        #     self.send_response(404)
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(f"Валюта не найдена: {code}".encode('utf-8'))
        #     return
        # except sqlite3.DatabaseError as e:
        #     self.send_response(500)
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write("The database is unavailable: {}".format(e).encode('utf-8'))

