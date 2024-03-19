from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController
from controller.rate_controller import RateController
from controller.rates_controller import RatesController
from service.service import ServiceExchange

routes = {'/currencies': CurrenciesController,
          '/currency': CurrencyController,
          '/exchangeRates': RatesController,
          '/exchangeRate': RateController,
          '/exchange': ServiceExchange}
