import sqlite3
from http.client import HTTPException


class ErrorResponse:
    @classmethod
    def error_response(cls, exception: Exception):
        error_code = 200
        error_message = "OK"
        if isinstance(exception, sqlite3.DatabaseError):
            error_code = 500
            error_message = f"The database is unavailable"
        if isinstance(exception, IndexError):
            error_code = 404
            error_message = f"Валюта не найдена"
        if isinstance(exception, IndexError):
            error_code = 404
            error_message = f"Обменный курс для пары не найден"
        if isinstance(exception, HTTPException):
            if exception.missing_fields == ['name', 'code', 'sign']:
                error_code = 400
                error_message = "Отсутствует обязательное поле формы: name, code, sign"
            elif exception.currency_not_found:
                error_code = 404
                error_message = "Валюта не найдена"
            elif exception.exchange_rate_not_found:
                error_code = 404
                error_message = "Обменный курс для пары не найден"
            else:
                error_code = 400
                error_message = "Запрос не верен"
        if isinstance(exception, sqlite3.IntegrityError):
            error_code = 409
            error_message = f"Валюта с этим кодом уже существует"
        return {error_code : error_message}





# print(isinstance(ErrorResponse.error_response(exception=sqlite3.DatabaseError()), ErrorResponse))
            # if isinstance(exception, (ValueError, TypeError)):
            #     error_message = f'Такой валюты нет в базе'
            #     self.send(404, {'error': error_message})
            # if isinstance(exception, MyError):
            #     error_message = f'Валютная пара с таким кодом уже существует'
            #     self.send(409, {'error': error_message})
        # except Exception as error:
        #     error_message = f'Возникла ошибка {error}'
        #     self.send(400, {'error': error_message})