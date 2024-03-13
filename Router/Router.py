from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController
from controller.rate_controller import RateController
from controller.rates_controller import RatesController
from service.service import ServiceExchange

routes = {

    '/currencies':
        {'method':
             {'get': CurrenciesController.do_GET(),
              'post': CurrenciesController.do_POST()},
         },
    '/currency':
        {'method':
             {'get': CurrencyController.do_GET()}
         },
    '/exchangeRates':
        {'method':
             {'get': RatesController.do_GET(),
              'post': RatesController.do_POST()}
         },
    '/exchangeRate':
        {'method':
             {'get': RateController.do_GET(),
              'patch': RateController.do_PATCH()}
         },
    '/exchange':
        {'method':
             {'get': ServiceExchange.do_GET()}
         }
}
