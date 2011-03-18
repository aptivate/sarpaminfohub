from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class PriceTest(SarpamTestCase):
    def test_fob_price_may_be_null(self):
        self.set_up_drc_ciprofloxacin(fob_price=None)
        
    def test_landed_price_may_be_null(self):
        self.set_up_drc_ciprofloxacin(landed_price=None)
    
    def test_fob_currency_may_be_null(self):
        self.set_up_drc_ciprofloxacin(fob_currency=None)
        
    def test_issue_unit_may_be_null(self):
        self.set_up_drc_ciprofloxacin(issue_unit=None)
        
    def test_landed_currency_may_be_null(self):
        self.set_up_drc_ciprofloxacin(landed_currency=None)
