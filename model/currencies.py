from dataclasses import dataclass


@dataclass
class Currency:
    """Класс валюты
   :@param id: id валюты
   :@param Code: Код валюты
   :@param full_name: Полное имя валюты
   :@param sign: Символ валюты
   """
    id: int
    code: str
    full_name: str
    sign: str
