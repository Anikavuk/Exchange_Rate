import sqlite3
from http.client import HTTPException

import dao.rates_DAO
import dto.service_DTO
import env

from controller.base_controller import BaseController
from dao.currencies_DAO import CurrencyDAO
from error_response import ErrorResponse


class ServiceExchange(BaseController):
    """Класс обработчик запроса GET http://localhost:8080/exchange?from=EUR&to=RUB&amount=10"""
    @staticmethod
    def find_rate(from_currency, to_currency):
        value = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            from_currency + to_currency)
        if value:
            return value['rate']
        if not value:
            value = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
                to_currency + from_currency)
            if value:
                return 1 / value['rate']
        value1 = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            'USD' + from_currency)
        value2 = dao.rates_DAO.ExchangeDAO(env.path_to_database).get_specific_exchange_rate(
            'USD' + to_currency)
        if not value1 or not value2:
            raise IndexError
        cross_rate = value2['rate'] / value1['rate']
        return cross_rate


    def do_GET(self, from_currency, to_currency, amount):
        try:
            rate = ServiceExchange.find_rate(from_currency, to_currency)
            response = dto.service_DTO.ServiceDTO(CurrencyDAO(env.path_to_database).find_by_code(from_currency).__dict__,
                                              CurrencyDAO(env.path_to_database).find_by_code(to_currency).__dict__,
                                              round(rate, 6),
                                              amount,
                                              round(float(rate * amount), 6)).to_dict()
            return response
        except HTTPException:
            return ErrorResponse.error_response(exception=HTTPException())
        except IndexError:
            return ErrorResponse.error_response(exception=IndexError())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=sqlite3.DatabaseError())

