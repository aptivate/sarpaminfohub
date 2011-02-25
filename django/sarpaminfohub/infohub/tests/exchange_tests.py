from sarpaminfohub.infohub.currency_exchange import CurrencyExchange
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
class ExchangeTest(SarpamTestCase):
    def test_currency_may_be_none(self):
        currency_exchange = CurrencyExchange()
        currency_exchange.exchange(local_price=1, currency=None, year=2009)