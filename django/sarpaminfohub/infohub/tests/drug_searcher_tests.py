from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.test_backend import TestBackend
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.models import ExchangeRate

class DrugSearcherTests(SarpamTestCase):
    
    def setup_exchange_rate(self):
        exchange_rate = ExchangeRate(symbol='NAD', rate='0.12314', year='2009')
        exchange_rate.save()
    
    def test_prices_converted_to_usd(self):
        self.setup_exchange_rate()
        
        test_backend = TestBackend()
        drug_searcher = DrugSearcher(test_backend)
        
        fob_price_in_nad = 58.64
        landed_price_in_nad = 67.44
        
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
         
        rows = drug_searcher.get_rows("amitriptyline")
        
        row = rows[0]
        
        self.assertEquals(fob_price_in_usd, row['fob_price'])
        self.assertEquals(landed_price_in_usd, row['landed_price'])

    def test_no_error_when_issue_unit_none(self):
        test_backend = TestBackend()
        drug_searcher = DrugSearcher(test_backend)
        rows = drug_searcher.get_rows("issue unit none")
        
        row = rows[0]
        
        self.assertEquals(None, row['fob_price'])
        self.assertEquals(None, row['landed_price'])
        