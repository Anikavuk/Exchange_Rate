from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController
from controller.rate_controller import RateController
from controller.rates_controller import RatesController
from service.service import ServiceExchange

# Словарь соответствия URL-адреса и класса - обработчика

routes = {'currency': CurrencyController,
          'currencies': CurrenciesController,
          'exchangeRate': RateController,
          'exchangeRates': RatesController,
          'exchange': ServiceExchange}
