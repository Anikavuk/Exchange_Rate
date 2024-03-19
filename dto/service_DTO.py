import env
from env import path_to_database
from  dao.currencies_DAO import CurrencyDAO
class ServiceDTO:

    def __init__(self, baseCurrency, targetCurrency, rate, amount, convertedAmount):
        """Класс обмена валют
        :@param baseCurrency: словарь базовой валюты
        :@param targetCurrency: словарь целевой валюты
        :@param rate: Курс обмена единицы базовой валюты к единице целевой валюты
        :@param amount: сумма валюты
        :@param convertedAmount: конвертация валюты
           """
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.amount = amount
        self.convertedAmount = convertedAmount

    def to_dict(self):
        return self.__dict__