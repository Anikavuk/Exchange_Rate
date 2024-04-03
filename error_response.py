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
    def __init__(self, value, message=None):
        self.value = value
        self.message = message
        super().__init__(self.message)


class CurrencyAlreadyExistsException(Exception): #Валюта уже существует, исключение
    def __init__(self, value, message=None):  # Валютная пара с таким кодом уже существует
        self.value = value
        self.message = message
        super().__init__(self.message)


class MissingFieldsException(HTTPException):  # Исключение отсутствующего поля
    def __init__(self, field, message=None):
        self.field = field
        self.message = message  # либо Код валютной пары отсутствует в адресе или Код валюты отсутствует в адресе
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
        elif isinstance(exception, IndexError):
            error_code = 404
            error_message = "Обменный курс для пары не найден"
        elif isinstance(exception, ExchangeRateNotFoundException):
        #     if exception.value == 'get_rate':
        #         error_code = 404
        #         error_message = "Обменный курс для пары не найден"
            if exception.value == 'post_rate':
                error_code = 404
                error_message = "Валютная пара отсутствует в базе данных"
        elif isinstance(exception, CurrencyAlreadyExistsException):
            if exception.value == 'code':
                error_code = 409
                error_message = "Валюта с таким кодом уже существует"
            else:
                error_code = 409
                error_message = "Валютная пара с таким кодом уже существует"
        elif isinstance(exception, MissingFieldsException):
            if exception.field == 'code':
                error_code = 400
                error_message = "Код валюты отсутствует в адресе"
            elif exception.field == 'full_name, code, sign':
                error_code = 400
                error_message = "Отсутствует нужное поле формы"
            elif exception.field == 'rate':
                error_code = 400
                error_message = "Коды валютной пары отсутствуют в адресе"
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
