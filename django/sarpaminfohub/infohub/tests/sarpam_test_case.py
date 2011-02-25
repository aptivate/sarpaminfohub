from django.test.testcases import TestCase
from sarpaminfohub.infohub.models import Formulation, Price, Country,\
    ExchangeRate

class SarpamTestCase(TestCase):
    def setup_drc_ciprofloxacin(self, fob_price="1.8", landed_price="2.085",
                                fob_currency='EUR', issue_unit=100,
                                landed_currency='EUR'):
        ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        ciprofloxacin.save()
        
        drc = Country(code='CD', name='Democratic Republic of Congo')
        drc.save()
        
        price = Price(formulation=ciprofloxacin, country=drc, 
                      fob_price=fob_price, fob_currency=fob_currency,
                      landed_price=landed_price, period=2009, 
                      issue_unit=issue_unit,
                      landed_currency=landed_currency)
        price.save()

    def setup_exchange_rate(self, symbol, rate, year):
        exchange_rate = ExchangeRate(symbol=symbol, rate=rate, year=year)
        exchange_rate.save()