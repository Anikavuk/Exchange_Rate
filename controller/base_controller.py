import sqlite3
from abc import ABC, abstractmethod
from http.client import HTTPException


class BaseController(ABC):

    @abstractmethod
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass

    def error_response(self, exception: Exception):
        error_code = 200
        error_message = "OK"
        if isinstance(exception, sqlite3.DatabaseError):
            error_code = 500
            error_message = f"The database is unavailable"
        if isinstance(exception, HTTPException):
            error_code = 400
            error_message = f"Код валюты отсутствует в адресе"
        if isinstance(exception, IndexError):
            error_code = 404
            error_message = f"Валюта не найдена"
        return {error_code : error_message}
            # if isinstance(exception, (ValueError, TypeError)):
            #     error_message = f'Такой валюты нет в базе'
            #     self.send(404, {'error': error_message})
            # if isinstance(exception, MyError):
            #     error_message = f'Валютная пара с таким кодом уже существует'
            #     self.send(409, {'error': error_message})
        # except Exception as error:
        #     error_message = f'Возникла ошибка {error}'
        #     self.send(400, {'error': error_message})
