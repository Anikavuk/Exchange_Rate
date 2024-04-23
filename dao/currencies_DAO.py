import sqlite3 as sq

import env
from model.currencies import *


class CurrencyDAO:
    """Класс для работы с базой данных таблицы currencies"""

    def __init__(self, path_to_database: object):
        self.__file = path_to_database

    def find_by_name(self, name: object) -> object:
        """
        Метод поиска валюты по Code из таблицы currencies
        :param code код валюты
        """
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM currencies WHERE FULL_Name LIKE ? || '%' OR FULL_Name LIKE '%' || ?", (name, name))
            response = cur.fetchall()
            conn.commit()
        return Currency(response[0][0], response[0][1], response[0][2], response[0][3])

    def all_currencies(self):
        """
        Метод выгрузки всех валют из таблицы currencies
        """
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM currencies')
            response = cur.fetchall()
            conn.commit()
        return [dict(id=row[0], name=row[2], code=row[1], sign=row[3]) for row in response]

    def save_currency(self, code, full_name, sign):
        """
        Метод сохранения новой валюты в таблицу currencies
        :param code код валюты
        :param full_name полное имя валюты
        :param sign символ валюты
        """
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('insert into currencies values (NULL, ?, ?, ?)', (code, full_name, sign))
            conn.commit()

    def find_by_code(self, code: object) -> object:
        """
        Метод поиска валюты по Code из таблицы currencies
        :param code код валюты
        """
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM currencies WHERE Code=?', (code,))
            response = cur.fetchall()
            conn.commit()
        return Currency(response[0][0], response[0][1], response[0][2], response[0][3])
