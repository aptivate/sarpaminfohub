from sarpaminfohub.infohub.django_backend import DjangoBackend
from decimal import Decimal
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class DjangoBackendTest(SarpamTestCase):
    
    def setUp(self):
        self.backend = DjangoBackend()
        
        self.expected_ciprofloxacin_results = \
            {"formulation":"ciprofloxacin 500mg tablet",
             "country": "Democratic Republic of Congo",
             "msh_price": Decimal("0.033"),
             "fob_price": Decimal("0.000003"),
             "landed_price": Decimal("0.000004"),
             "fob_currency": 'EUR',
             "period": 2009,
             "issue_unit":100,
             "landed_currency": 'EUR',
             'url': '/formulation/1/'}

        self.ciprofloxacin = self.set_up_drc_ciprofloxacin(fob_price=Decimal("0.000003"),
                                     landed_price=Decimal("0.000004"))
        
        biofloxx = self.set_up_biofloxx(self.ciprofloxacin)
        suppliers = self.set_up_suppliers()
        manufacturers = self.set_up_manufacturers()

        biofloxx.suppliers = suppliers
        biofloxx.manufacturers = manufacturers
        biofloxx.save()
    
    def test_search_for_ciprofloxacin_returns_ciprofloxacin_500mg(self):
        self.set_up_msh_for_ciprofloxacin()
        results = self.backend.get_formulations_that_match('ciprofloxacin')
        self.assertEquals(self.expected_ciprofloxacin_results, results[0])

    def test_search_is_case_insensitive(self):
        results = self.backend.get_formulations_that_match('CIPROFLOXACIN')
        first_row = results[0]
        self.assertEquals(self.expected_ciprofloxacin_results['formulation'],
                          first_row['formulation'])

    def get_first_row_of_prices_with_formulation_id_1(self):
        rows = self.backend.get_prices_for_formulation_with_id(1)
        return rows[0]

    def check_column_matches_expected_field_with_name(self, name):
        first_row = self.get_first_row_of_prices_with_formulation_id_1()
        self.assertEquals(self.expected_ciprofloxacin_results[name],
                          first_row[name])

    def test_ciprofloxacin_country_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('country')

    def test_ciprofloxacin_fob_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('fob_price')

    def test_ciprofloxacin_landed_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('landed_price')

    def test_ciprofloxacin_fob_currency_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('fob_currency')
        
    def test_ciprofloxacin_period_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('period')
        
    def test_ciprofloxacin_issue_unit_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('issue_unit')
        
    def test_ciprofloxacin_issue_landed_currency_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('landed_currency')

    def test_formulation_name_can_be_retrieved_by_id(self):
        name = self.backend.get_formulation_name_with_id(1)
        self.assertEquals("ciprofloxacin 500mg tablet", name)

    def test_formulation_msh_can_be_retrieved_by_id(self):
        self.set_up_msh_for_ciprofloxacin()
        msh_price = self.backend.get_formulation_msh_with_id(1)
        self.assertEquals(self.expected_ciprofloxacin_results['msh_price'], 
                          msh_price)

    def test_ciprofloxacin_product_can_be_retrieved_by_id(self):
        products = self.backend.get_products_based_on_formulation_with_id(1)
        biofloxx = products[0]
        
        self.assertEquals("BIOFLOXX 500 MG", biofloxx['product'])

    def test_ciprofloxacin_suppliers_can_be_retrieved_by_id(self):
        products = self.backend.get_products_based_on_formulation_with_id(1)
        biofloxx = products[0]
        
        biotech_laboratories = {'name' : "Biotech Laboratories",
                                'url' : "/suppliers/1/"}
        
        camox = {'name' : "Camox Pharmaceuticals (Pty) Ltd",
                 'url' : "/suppliers/2/"}
        
        expected_suppliers = [biotech_laboratories, camox]
        
        self.assertEquals(expected_suppliers, biofloxx['suppliers'])

    def test_ciprofloxacin_manufacturers_can_be_retrieved_by_id(self):
        products = self.backend.get_products_based_on_formulation_with_id(1)
        biofloxx = products[0]
        
        unique_pharmaceuticals = {'name' : "Unique Pharmaceutical Labs, India"}
        
        expected_manufacturers = [unique_pharmaceuticals]
        
        self.assertEquals(expected_manufacturers, biofloxx['manufacturers'])


    def test_supplier_name_can_be_retrieved_by_id(self):
        supplier_name = self.backend.get_name_of_supplier_with_id(1)
        self.assertEquals("Biotech Laboratories", supplier_name)

    def test_msh_price_none_for_formulation_with_no_msh(self):
        first_row = self.get_first_row_of_prices_with_formulation_id_1()
        self.assertEquals(None, first_row['msh_price'])

    def test_msh_price_none_for_matching_formulation_with_no_msh(self):
        results = self.backend.get_formulations_that_match('ciprofloxacin')
        first_row = results[0]
        self.assertEquals(None, first_row['msh_price'])
