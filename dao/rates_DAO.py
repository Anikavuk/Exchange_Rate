import sqlite3 as sq

import dao.currencies_DAO
import dto.currencies_DTO
import dto.rates_DTO
import env


class ExchangeDAO:
    """Класс для работы с базой данных таблицы exchange_rates"""

    def __init__(self, db_file):
        self.__file = db_file

    def get_specific_exchange_rate(self, code: object) -> object:
        """Метод получения конкретного обменного курса валют.
        :@param code - код валюты, например, 'USDEUR'
        """
        base = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code[:3])
        target = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(code[3:])
        baseCurrency = dto.currencies_DTO.CurrencyDTO(base.id, base.full_name, base.code, base.sign).to_dict()
        targetCurrency = dto.currencies_DTO.CurrencyDTO(target.id, target.full_name, target.code, target.sign).to_dict()
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM exchange_rates WHERE BaseCurrencyld=? AND TargetCurrencyld=?',
                        (base.id, target.id))
            response = cur.fetchall()
            conn.commit()
        if not response:
            return []
        return dto.rates_DTO.ExchangeRatesDTO(response[0][0], baseCurrency, targetCurrency, response[0][3]).to_dict()

    def all_exchange_rates(self):
        """Метод получения курса всех валют"""
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM exchange_rates')
            response = cur.fetchall()
            conn.commit()
        data = []
        for ilem in response:
            data.append(dto.rates_DTO.ExchangeRatesDTO(ilem[0],
                                                       self.find_by_id(ilem[1]),
                                                       self.find_by_id(ilem[2]),
                                                       ilem[3]).to_dict())
        return data

    def find_by_id(self, id: int):
        """
        Метод поиска валюты по айди из таблицы currencies
        :@param id айди валюты
        """
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM currencies WHERE id=?', (id,))
            response = cur.fetchall()
            conn.commit()
        return dto.currencies_DTO.CurrencyDTO(response[0][0], response[0][1], response[0][2], response[0][3]).to_dict()

    def save_rate(self, baseCode, targetCode, rate):
        """метод сохранения курса
        :@param baseCode: Code базовой валюты
        :@param targetCode: Code целевой валюты
        :@param rate: обменный курс
        """
        baseCurrency = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(baseCode)
        targetCurrency = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(targetCode)
        base = baseCurrency.id
        target = targetCurrency.id
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            query = 'INSERT INTO exchange_rates (BaseCurrencyld, TargetCurrencyld, Rate) \
                     SELECT ?, ?, ? \
                     WHERE NOT EXISTS (SELECT 1 FROM exchange_rates WHERE BaseCurrencyld = ? AND TargetCurrencyld = ?)'
            cur.execute(query, (base, target, rate, base, target))
            conn.commit()

    def update_rate(self, baseCode, targetCode, rate):
        """метод изенения курса валют в базе данных
        :@param baseCode: Code базовой валюты
        :@param targetCode: Code целевой валюты
        :@param rate: новый обменный курс
        """
        baseCurrency = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(baseCode)
        targetCurrency = dao.currencies_DAO.CurrencyDAO(env.path_to_database).find_by_code(targetCode)
        base = baseCurrency.id
        target = targetCurrency.id
        with sq.connect(self.__file) as conn:
            cur = conn.cursor()
            query = 'UPDATE exchange_rates \
                     SET Rate = ? \
                     WHERE BaseCurrencyld = ? AND TargetCurrencyld = ?'
            cur.execute(query, (rate, base, target))
            conn.commit()
