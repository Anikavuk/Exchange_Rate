import sqlite3

from werkzeug.exceptions import HTTPException


class DatabaseErrorException(Exception):
    def __init__(self, message="База данных недоступна"):
        self.message = message
        super().__init__(self.message)


class CurrencyNotFoundException(Exception):
    def __init__(self, message="Валюта не найдена"):
        self.message = message
        super().__init__(self.message)


class ExchangeRateNotFoundException(Exception):
    def __init__(self, message="Обменный курс для пары не найден"):  # либо Валютная пара отсутствует в базе данных
        self.message = message
        super().__init__(self.message)


class MissingFieldsException(HTTPException):  # Исключение отсутствующего поля
    def __init__(self, fields, message):
        # super().__init__(fields)
        self.fields = fields
        self.message = 'Данные отсутствуют в адресе:'  # либо Код валютной пары отсутствует в адресе или Код валюты отсутствует в адресе


class CurrencyAlreadyExistsException(Exception):
    def __init__(self, message="Валюта уже существует"):  # Валютная пара с таким кодом уже существует
        self.message = message
        super().__init__(self.message)


class ErrorResponse:
    @classmethod
    def error_response(cls, exception: Exception):
        error_code = 200
        error_message = "OK"
        if isinstance(exception, DatabaseErrorException):
            error_code = 500
            error_message = "База данных недоступна"
        elif isinstance(exception, CurrencyNotFoundException):
            error_code = 404
            error_message = "Валюта не найдена"
        elif isinstance(exception, ExchangeRateNotFoundException):
            error_code = 404
            error_message = "Обменный курс для пары не найден"
        elif isinstance(exception, MissingFieldsException):
            error_code = 400
            error_message = 'Данные отсутствуют в адресе:'
        elif isinstance(exception, sqlite3.IntegrityError):
            error_code = 409
            error_message = "A currency with this code already exists"
        return {error_code: error_message}

        # elif isinstance(exception, MissingFieldsException):
        #     if exception.fields == ['name', 'code', 'sign']:
        #         error_code = 400
        #         error_message = "The required form field is missing: name, code, sign"
        #     else:
        #         error_code = 400
        #         error_message = "Запрос не верен"
# class ErrorResponse:
#     @classmethod
#     def error_response(cls, exception: Exception):
#         error_code = 200
#         error_message = "OK"
#         if isinstance(exception, sqlite3.DatabaseError):
#             error_code = 500
#             error_message = f"The database is unavailable"
#         if isinstance(exception, IndexError):
#             error_code = 404
#             error_message = f"Валюта не найдена"
#         if isinstance(exception, IndexError):
#             error_code = 404
#             error_message = f"Обменный курс для пары не найден"
#         # if isinstance(exception, HTTPException):
#         #     if exception.missing_fields == ['name', 'code', 'sign']:
#         #         error_code = 400
#         #         error_message = "Отсутствует обязательное поле формы: name, code, sign"
        #     elif exception.currency_not_found:
        #         error_code = 404
        #         error_message = "Валюта не найдена"
        #     elif exception.exchange_rate_not_found:
        #         error_code = 404
        #         error_message = "Обменный курс для пары не найден"
        #     else:
        #         error_code = 400
        # #         error_message = "Запрос не верен"
        # if isinstance(exception, sqlite3.IntegrityError):
        #     error_code = 409
        #     error_message = f"Валюта с этим кодом уже существует"
        # return {error_code: error_message}

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
