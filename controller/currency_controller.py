import sqlite3

from loguru import logger

import dao.currencies_DAO
import dto.currencies_DTO
import env
from controller.base_controller import BaseController
from error_response import ErrorResponse, DatabaseErrorException, \
    MissingFieldsException, CurrencyNotFoundException

logger.add('errors_Currency.log', format="{time} {level} {message}", level="ERROR", serialize=True)


class CurrencyController(BaseController):
    """Класс обработчик запроса http://localhost:8080/currency/USD"""

    @logger.catch
    def do_GET(self, code):
        """
        Метод получения конкретной валюты
        """
        try:
            if code is None or len(code) != 3:
                raise MissingFieldsException('code')
            data = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code)
            response = dto.currencies_DTO.CurrencyDTO(data.id, data.full_name, data.code, data.sign).to_dict()
            logger.error(data)
            return response
        except MissingFieldsException:
            return ErrorResponse.error_response(exception=MissingFieldsException('code'))
        except IndexError:
            return ErrorResponse.error_response(exception=CurrencyNotFoundException())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())
