import sqlite3

from loguru import logger

import dao.currencies_DAO
import dto.currencies_DTO
import env
from controller.base_controller import BaseController
from dao.currencies_DAO import CurrencyDAO
from error_response import ErrorResponse, DatabaseErrorException, MissingFieldsException, CurrencyAlreadyExistsException

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
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    @logger.catch
    def do_POST(self, post_data_dict):
        logger.debug(post_data_dict)
        try:
            full_name = post_data_dict.get("name")
            code = post_data_dict.get("code")
            sign = post_data_dict.get("sign")
            if full_name is None or code is None or sign is None:
                raise MissingFieldsException('full_name, code, sign')

            save_response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).save_currency(code, full_name, sign)
            response = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
            data = dto.currencies_DTO.CurrencyDTO(response.id, response.full_name, response.code,
                                                  response.sign).to_dict()
            return data
        except MissingFieldsException:
            return ErrorResponse.error_response(exception=MissingFieldsException('full_name, code, sign'))
        except sqlite3.IntegrityError:
            return ErrorResponse.error_response(exception=CurrencyAlreadyExistsException('code'))
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())
