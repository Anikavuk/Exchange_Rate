import sqlite3

from loguru import logger

import dao.rates_DAO
import env
from controller.base_controller import BaseController
from error_response import ErrorResponse, DatabaseErrorException, MissingFieldsException, ExchangeRateNotFoundException

logger.add('rates_controller.log', format="{time} {level} {message}", level="DEBUG", serialize=True)


class RatesController(BaseController):
    """Класс - обработчик запроса
    GET http://localhost:8080/exchangeRates
    POST http://localhost:8080/exchangeRates"""

    @logger.catch
    def do_GET(self):
        try:
            response = dao.rates_DAO.ExchangeDAO(env.path_to_database).all_exchange_rates()
            logger.debug(response)
            return response
        except IndexError:
            return ErrorResponse.error_response(exception=IndexError())
        except sqlite3.OperationalError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    @logger.catch
    def do_POST(self, post_data_dict):
        try:
            baseCurrency = post_data_dict.get("baseCurrencyCode")
            targetCurrency = post_data_dict.get("targetCurrencyCode")
            rate = post_data_dict.get("rate")
            if baseCurrency is None or targetCurrency is None or rate is None:
                raise MissingFieldsException('full_name, code, sign')

            save_rate = dao.rates_DAO.ExchangeDAO(env.path_to_database).save_rate(baseCurrency, targetCurrency, rate)
            response = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
                baseCurrency + targetCurrency)
            return response
        except MissingFieldsException:
            return ErrorResponse.error_response(exception=MissingFieldsException('full_name, code, sign'))
        except IndexError:
            return ErrorResponse.error_response(exception=ExchangeRateNotFoundException('post_rate'))
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())
