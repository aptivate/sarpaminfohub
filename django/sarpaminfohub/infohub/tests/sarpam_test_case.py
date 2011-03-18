from django.test.testcases import TestCase
from sarpaminfohub.infohub.models import Formulation, Price, Country,\
    ExchangeRate, Product, Supplier, MSHPrice
from decimal import Decimal

class SarpamTestCase(TestCase):
    def set_up_biofloxx(self, formulation, suppliers=[]):
        biofloxx = Product(formulation=formulation, name="BIOFLOXX 500 MG")
        biofloxx.save()

        biofloxx.suppliers = suppliers
        biofloxx.save()
    
    def set_up_drc_ciprofloxacin(self, fob_price="1.8", landed_price="2.085",
                                fob_currency='EUR', issue_unit=100,
                                landed_currency='EUR'):
        self.ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        self.ciprofloxacin.save()

        drc = Country(code='CD', name='Democratic Republic of Congo')
        drc.save()

        price = Price(formulation=self.ciprofloxacin, country=drc, 
                      fob_price=fob_price, fob_currency=fob_currency,
                      landed_price=landed_price, period=2009, 
                      issue_unit=issue_unit,
                      landed_currency=landed_currency)
        price.save()
        
        return self.ciprofloxacin
        
    def set_up_msh_for_ciprofloxacin(self):
        msh = MSHPrice(formulation=self.ciprofloxacin, period=2009, 
                       price=Decimal("0.033"))
        msh.save()

    def set_up_suppliers_of_formulation(self, formulation):
        biotech_laboratories = Supplier(name="Biotech Laboratories")
        biotech_laboratories.save()
        
        camox_pharmaceuticals = Supplier(name="Camox Pharmaceuticals (Pty) Ltd")
        camox_pharmaceuticals.save()
        
        suppliers = [biotech_laboratories, camox_pharmaceuticals]
        
        self.set_up_biofloxx(formulation, suppliers)

    def set_up_exchange_rate(self, symbol, rate, year):
        exchange_rate = ExchangeRate(symbol=symbol, rate=rate, year=year)
        exchange_rate.save()

    def set_up_exchange_rate_for_nad(self):
        self.set_up_exchange_rate(symbol='NAD', rate=0.12314, year=2009)
    
    def set_up_exchange_rate_for_usd(self):
        self.set_up_exchange_rate(symbol='USD', rate=1.03, year=2007)
        
    def set_up_exchange_rate_for_eur(self):
        self.set_up_exchange_rate(symbol='EUR', rate=1.39071, year=2009)

    def set_up_exchange_rate_for_zar(self):
        self.set_up_exchange_rate(symbol='ZAR', rate='0.11873', year='2009')
