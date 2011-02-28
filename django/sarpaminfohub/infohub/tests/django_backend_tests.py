from sarpaminfohub.infohub.django_backend import DjangoBackend
from decimal import Decimal
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class DjangoBackendTest(SarpamTestCase):
    
    def setUp(self):
        self.backend = DjangoBackend()
        
        self.expected_ciprofloxacin_results = \
            {"formulation":"ciprofloxacin 500mg tablet",
                           "country": "Democratic Republic of Congo",
                           "fob_price": Decimal("0.000003"), 
                           "landed_price": Decimal("0.000004"),
                           "fob_currency": 'EUR',
                           "period": 2009,
                           "issue_unit":100,
                           "landed_currency": 'EUR'}

        self.setup_drc_ciprofloxacin(fob_price=Decimal("0.000003"), 
                                     landed_price=Decimal("0.000004"))
        
    
    def test_search_for_ciprofloxacin_returns_ciprofloxacin_500mg(self):
        results = self.backend.search('ciprofloxacin')
        
        self.assertEquals(self.expected_ciprofloxacin_results, results[0])

    def test_search_is_case_sensitive(self):
        results = self.backend.search('CIPROFLOXACIN')
        
        self.assertEquals(self.expected_ciprofloxacin_results, results[0])
