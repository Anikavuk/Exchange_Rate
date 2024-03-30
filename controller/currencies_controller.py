import json
import sqlite3
import urllib.request
from http.client import HTTPException

import env
import dto.currencies_DTO
import dao.currencies_DAO
from urllib.parse import parse_qs

from controller.base_controller import BaseController
from dao.currencies_DAO import CurrencyDAO
from loguru import logger

from error_response import ErrorResponse

logger.add('errors.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


class CurrenciesController(BaseController):
    """Класс обработчик запроса GET http://localhost:8080/currencies
    POST http://localhost:8080/currencies"""
    @logger.catch
    def do_GET(self):
        try:
            response = CurrencyDAO(env.path_to_database).all_currencies()
            logger.debug(response)
            return response
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=sqlite3.DatabaseError())

    @logger.catch
    def do_POST(self, post_data_dict):
        try:
            full_name = post_data_dict.get("name")
            code = post_data_dict.get("code")
            sign = post_data_dict.get("sign")
        # if full_name is None or code is None or sign is None:
        #     self.send_response(400)
        #     self.send_header('Content-Type', "application/json")
        #     self.end_headers()
        #     self.wfile.write(f"The required form field is missing: name, code, sign".encode('utf-8'))
        #     return

            save_response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).save_currency(code, full_name,sign)
            response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
            data = dto.currencies_DTO.CurrencyDTO(response.id, response.full_name, response.code, response.sign).to_dict()
            return data
        except HTTPException:
            return ErrorResponse.error_response(exception=HTTPException())
        except sqlite3.IntegrityError:
            return ErrorResponse.error_response(exception=sqlite3.IntegrityError())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=sqlite3.DatabaseError())