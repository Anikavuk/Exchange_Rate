import sqlite3
from http.client import HTTPException

from loguru import logger

import dao.currencies_DAO
import dto.currencies_DTO
import env
from controller.base_controller import BaseController
from error_response import ErrorResponse

logger.add('errors_Currency.log', format="{time} {level} {message}", level="ERROR", serialize=True)


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
                return response
            else:
                return ErrorResponse.error_response(exception=HTTPException())
        except IndexError:
            return ErrorResponse.error_response(exception=IndexError())
        except sqlite3.DatabaseError:
            return ErrorResponse.error_response(exception=sqlite3.DatabaseError())


a = CurrencyController()
print(a.do_GET('UUU'))
# print(a.do_GET('USD')) #этот работает
print(a.do_GET(""))





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
