from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.models import Formulation, Price

class PriceTest(SarpamTestCase):
    def test_fob_price_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.fob_price)
        
    def test_landed_price_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.landed_price)
    
    def test_fob_currency_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.fob_currency)
        
    def test_issue_unit_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.issue_unit)
        
    def test_landed_currency_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.landed_currency)

    def test_incoterm_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.incoterm)
        
    def test_supplier_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.supplier)
        
    def test_supplier_country_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.supplier_country)

    def test_manufacturer_country_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.manufacture_country)
    
    def test_volume_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.volume)

    def test_country_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.country)

    def test_period_may_be_null(self):
        price = self.set_up_and_return_price()
        self.assertEquals(None, price.period)

    def test_incoterm_may_be_null_in_record(self):
        price = self.set_up_and_return_price()
        record = price.get_record()
        self.assertEquals(None, record['incoterm'])

    def set_up_and_return_price(self):
        ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        ciprofloxacin.save()
        
        price = Price(formulation=ciprofloxacin)
        price.save()
        
        return price
