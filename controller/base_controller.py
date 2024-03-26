import sqlite3
from abc import ABC, abstractmethod


class BaseController(ABC):

    @abstractmethod
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass

    def error_response(self, exception: Exception):

        try:
            if isinstance(exception, sqlite3.DatabaseError):
                error_message = f'возникла ошибка при работе с базой данных {exception}'
                self.send(500, {'error': error_message})
            if isinstance(exception, (ValueError, TypeError)):
                error_message = f'Такой валюты нет в базе'
                self.send(404, {'error': error_message})
            if isinstance(exception, HTTPException):
                error_message = f'Некорректный запрос'
                self.send(400, {'error': error_message})
            if isinstance(exception, (IndexError, AttributeError)):
                error_message = f'Не хватает данных для выполнения'
                self.send(400, {'error': error_message})
            if isinstance(exception, MyError):
                error_message = f'Валютная пара с таким кодом уже существует'
                self.send(409, {'error': error_message})
        except Exception as error:
            error_message = f'Возникла ошибка {error}'
            self.send(400, {'error': error_message})
