class ExchangeRatesDTO:
    """Класс курса валют DTO
    :@param id: id курса
    :@param BaseCurrencyld: ID базовой валюты
    :@param TargetCurrencyld: ID целевой валюты
    :@param Rate: Курс обмена единицы базовой валюты к единице целевой валюты
   """

    def __init__(self, id, baseCurrency, targetCurrency, rate):
        self.id = id
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate

    def to_dict(self):
        return self.__dict__