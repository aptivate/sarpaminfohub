from sarpaminfohub.infohub.django_backend import DjangoBackend
from decimal import Decimal
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class DjangoBackendTest(SarpamTestCase):
    def test_search_for_ciprofloxacin_returns_ciprofloxacin_500mg(self):
        self.setup_drc_ciprofloxacin(fob_price=Decimal("0.000003"), 
                                     landed_price=Decimal("0.000004"))
        
        backend = DjangoBackend()
        
        results = backend.search('ciprofloxacin')
        
        self.assertEquals({"formulation":"ciprofloxacin 500mg tablet",
                           "country": "Democratic Republic of Congo",
                           "fob_price": Decimal("0.000003"), 
                           "landed_price": Decimal("0.000004"),
                           "fob_currency": 'EUR',
                           "period": 2009,
                           "issue_unit":100,
                           "landed_currency": 'EUR'},
                          results[0])
