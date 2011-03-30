from django.test.testcases import TestCase
from sarpaminfohub.infohub.models import Formulation, Price, Country, \
    ExchangeRate, Product, MSHPrice, Incoterm
from decimal import Decimal

class SarpamTestCase(TestCase):
    def __init__(self, method_name):
        self.ciprofloxacin = None
        TestCase.__init__(self, method_name)
    
    def set_up_and_return_biofloxx(self, formulation):
        biofloxx = Product(formulation=formulation, name="BIOFLOXX 500 MG")
        biofloxx.save()

        return biofloxx
    
    def set_up_and_return_drc_ciprofloxacin(self, fob_price="1.8", landed_price="2.085",
                                fob_currency='EUR', issue_unit=100,
                                landed_currency='EUR',
                                volume=None):
        self.ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        self.ciprofloxacin.save()

        drc = Country(code='CD', name='Democratic Republic of Congo')
        drc.save()

        incoterm = Incoterm(name="CIF")
        incoterm.save()

        price = Price(formulation=self.ciprofloxacin, country=drc, 
                      fob_price=fob_price, fob_currency=fob_currency,
                      landed_price=landed_price, period=2009, 
                      issue_unit=issue_unit,
                      landed_currency=landed_currency, incoterm=incoterm)
        price.save()
        
        return self.ciprofloxacin
        
    def set_up_msh_for_ciprofloxacin(self):
        msh = MSHPrice(formulation=self.ciprofloxacin, period=2009, 
                       price=Decimal("0.033"))
        msh.save()

    def set_up_exchange_rate(self, symbol, rate, year):
        exchange_rate = ExchangeRate(symbol=symbol, rate=rate, year=year)
        exchange_rate.save()

    def set_up_exchange_rate_for_nad(self):
        self.set_up_exchange_rate(symbol='NAD', rate=0.12314, year=2009)
    
    def set_up_exchange_rate_for_usd(self):
        self.set_up_exchange_rate(symbol='USD', rate=1.03, year=2007)
        self.set_up_exchange_rate(symbol='USD', rate=1.0, year=2009)
        
    def set_up_exchange_rate_for_eur(self):
        self.set_up_exchange_rate(symbol='EUR', rate=1.39071, year=2009)

    def set_up_exchange_rate_for_zar(self):
        self.set_up_exchange_rate(symbol='ZAR', rate='0.11873', year='2009')

    def contains(self, string_to_search, sub_string):
        return string_to_search.find(sub_string) > -1
