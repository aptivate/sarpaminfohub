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

    def get_first_row_of_prices_with_formulation_id_1(self):
        rows = self.backend.get_prices_for_formulation_with_id(1)
        
        return rows[0]

    def check_column_matches_expected_field_with_name(self, name):
        first_row = self.get_first_row_of_prices_with_formulation_id_1()
        self.assertEquals(self.expected_ciprofloxacin_results[name],\
                          first_row[name])

    def test_ciprofloxacin_country_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('country')

    def test_ciprofloxacin_fob_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('fob_price')

    def test_ciprofloxacin_landed_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('landed_price')

    def test_formulation_name_can_be_retrieved_by_id(self):
        name = self.backend.get_formulation_name_with_id(1)
        self.assertEquals("ciprofloxacin 500mg tablet", name)
