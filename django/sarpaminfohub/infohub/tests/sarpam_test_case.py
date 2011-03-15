from django.test.testcases import TransactionTestCase
from sarpaminfohub.infohub.models import Formulation, Price, Country,\
    ExchangeRate, MSHPrice

class SarpamTestCase(TransactionTestCase):
    def setup_drc_ciprofloxacin(self, fob_price="1.8", landed_price="2.085",
                                msh_price="0.033",
                                fob_currency='EUR', issue_unit=100,
                                landed_currency='EUR'):
        ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        ciprofloxacin.save()

        drc = Country(code='CD', name='Democratic Republic of Congo')
        drc.save()

        msh = MSHPrice(formulation=ciprofloxacin, period=2009, price=msh_price)
        msh.save()

        price = Price(formulation=ciprofloxacin, country=drc, 
                      fob_price=fob_price, fob_currency=fob_currency,
                      landed_price=landed_price, period=2009, 
                      issue_unit=issue_unit,
                      landed_currency=landed_currency)
        price.save()

    def setup_exchange_rate(self, symbol, rate, year):
        exchange_rate = ExchangeRate(symbol=symbol, rate=rate, year=year)
        exchange_rate.save()

    def setup_exchange_rate_for_nad(self):
        self.setup_exchange_rate(symbol='NAD', rate=0.12314, year=2009)
    
    def setup_exchange_rate_for_usd(self):
        self.setup_exchange_rate(symbol='USD', rate=1.03, year=2007)
        
    def setup_exchange_rate_for_eur(self):
        self.setup_exchange_rate(symbol='EUR', rate=1.39071, year=2009)
    

    def setup_exchange_rate_for_zar(self):
        self.setup_exchange_rate(symbol='ZAR', rate='0.11873', year='2009')
