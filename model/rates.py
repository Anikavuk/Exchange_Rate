import decimal
from dataclasses import dataclass


@dataclass()
class ExchangeRate:
    """Класс курса валют
    :@param id: id курса
    :@param BaseCurrencyld: ID базовой валюты
    :@param TargetCurrencyld: ID целевой валюты
    :@param Rate: Курс обмена единицы базовой валюты к единице целевой валюты
   """
    ID: int
    BaseCurrencyld: dict
    TargetCurrencyld: dict
    Rate: decimal
