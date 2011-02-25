from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class PriceTest(SarpamTestCase):
    def test_fob_price_may_be_null(self):
        self.setup_drc_ciprofloxacin(fob_price=None)
        
    def test_landed_price_may_be_null(self):
        self.setup_drc_ciprofloxacin(landed_price=None)
    
        