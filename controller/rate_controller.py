import sqlite3
import sys

from loguru import logger

import dao.rates_DAO
import env
from controller.base_controller import BaseController
from error_response import ErrorResponse, MissingFieldsException, ExchangeRateNotFoundException, DatabaseErrorException

logger.add(sys.stdout, format="{time} {level} {message}", level="ERROR", serialize=True)


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
                if not response:
                    raise IndexError
                return response
            else:
                raise MissingFieldsException('rate')
        except MissingFieldsException:
            return ErrorResponse.error_response(exception=MissingFieldsException('rate'))
        except IndexError:
            return ErrorResponse.error_response(exception=IndexError())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    def do_PATCH(self, name_currencies, post_data_dict):
        try:
            if name_currencies:
                rate = post_data_dict.get("rate")
                if rate is None:
                    raise MissingFieldsException('full_name, code, sign')
                currencies = name_currencies.split(" ")
                baseName = currencies[0]
                targetName = currencies[-1]
                save_response = dao.rates_DAO.ExchangeDAO(env.path_to_database).update_rate_by_currency_name(baseName,
                                                                                            targetName,
                                                                                            rate)
                response = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_exchange_rate_by_name(baseName, targetName)
                return response
            else:
                raise MissingFieldsException('full_name, code, sign')
        except MissingFieldsException:
            return ErrorResponse.error_response(exception=MissingFieldsException('full_name, code, sign'))
        except IndexError:
            return ErrorResponse.error_response(exception=ExchangeRateNotFoundException('post_rate'))
        except sqlite3.DatabaseError:
                return ErrorResponse.error_response(exception=DatabaseErrorException())
