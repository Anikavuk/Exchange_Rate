class CurrencyDTO:
    """Класс шаблон DTO для единного вида выгрузки валюты
    :@param id: id валюты
    :@param Code: Код валюты
    :@param full_name: Полное имя валюты
    :@param sign: Символ валюты
   """

    def __init__(self, id, name, code, sign):
        self.id = id
        self.name = name
        self.code = code
        self.sign = sign

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными валюты"""
        return self.__dict__
