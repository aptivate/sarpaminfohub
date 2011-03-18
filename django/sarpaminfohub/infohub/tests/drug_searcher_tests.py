# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.test_backend import TestBackend
from sarpaminfohub.infohub.drug_searcher import DrugSearcher

class DrugSearcherTest(SarpamTestCase):
    def setUp(self):
        test_backend = TestBackend()
        self.drug_searcher = DrugSearcher(test_backend)
    
    def test_prices_converted_to_usd(self):
        self.setup_exchange_rate_for_nad()
        
        fob_price_in_nad = 58.64
        landed_price_in_nad = 67.44
        
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
         
        rows = self.drug_searcher.get_formulations_that_match("amitriptyline")
        
        row = rows[0]
        
        self.assertEquals(fob_price_in_usd, row['fob_price'])
        self.assertEquals(landed_price_in_usd, row['landed_price'])

    def test_no_error_when_issue_unit_none(self):
        rows = self.drug_searcher.get_formulations_that_match("issue unit none")
        row = rows[0]

        self.assertEquals(None, row['fob_price'])
        self.assertEquals(None, row['landed_price'])
        
    def test_prices_for_amoxycillin_is_converted_to_usd(self):
        self.setup_exchange_rate_for_nad()
        
        fob_price_in_nad = 58.64
        landed_price_in_nad = 67.44
        
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
        
        rows = self.drug_searcher.get_prices_for_formulation_with_id("amitriptyline")
        row = rows[0]
        
        self.assertEquals(fob_price_in_usd, row['fob_price'])
        self.assertEquals(landed_price_in_usd, row['landed_price'])

    def test_gets_formulation_name_from_backend_given_id(self):
        name = self.drug_searcher.get_formulation_name_with_id(1)
        self.assertEquals("amitriptyline 25mg tablet", name)

    def get_formulations_that_match_amox(self):
        self.setup_exchange_rate_for_eur()
        self.setup_exchange_rate_for_nad()
        self.setup_exchange_rate_for_usd()
        
        return self.drug_searcher.get_formulations_that_match("amox")
        

    def test_matching_formulations_grouped_by_formulation_name(self):
        formulations = self.get_formulations_that_match_amox()

        self.assertEquals(3, len(formulations))
        amoxycillin125 = formulations[0]
        amoxycillin500 = formulations[1]
        tamoxifen = formulations[2]

        self.assertEquals(amoxycillin125['formulation'], 
                          "amoxycillin 125mg/5ml suspension")
        self.assertEquals(amoxycillin500['formulation'],
                          "amoxycillin 500mg tablet/capsule")
        self.assertEquals(tamoxifen['formulation'],
                          "tamoxifen 20mg tablet")

    def test_matching_formulations_include_median_fob_price(self):
        formulations = self.get_formulations_that_match_amox()

        # fob prices are:
        # Angola None
        # DRC 0.004
        # Namibia 0.005
        # Botswana 0.009

        amoxycillin125 = formulations[0]

        fob_price_for_namibia = 4.36
        nad_exchange_rate = 0.12314
        issue_unit = 100

        expected_median = (fob_price_for_namibia * nad_exchange_rate) / issue_unit

        self.assertAlmostEquals(expected_median, amoxycillin125['fob_price'])

    def test_matching_formulations_include_median_landed_price(self):
        formulations = self.get_formulations_that_match_amox()

        amoxycillin125 = formulations[0]

        landed_price_for_namibia = 4.93
        nad_exchange_rate = 0.12314
        issue_unit = 100

        expected_median = (landed_price_for_namibia * nad_exchange_rate) / issue_unit

        self.assertAlmostEquals(expected_median, amoxycillin125['landed_price'])

    def test_none_returned_for_median_of_empty_list(self):
        empty_list = []
        median = self.drug_searcher.get_median(empty_list)
        self.assertEquals(None, median)

    def test_middle_value_returned_for_median_of_list_with_odd_length(self):
        price_list = [0.09, 0.05, 0.14]
        median = self.drug_searcher.get_median(price_list)
        self.assertAlmostEquals(0.09, median)
        
    def test_average_of_middle_values_returned_for_median_of_list_with_even_length(self):
        price_list = [0.04, 0.05, 0.14, 0.07]
        median = self.drug_searcher.get_median(price_list)
        self.assertAlmostEquals(0.06, median)

    def test_none_values_ignored_when_calculating_median_fob_price_of_list(self):
        price_list = [{'fob_price':None, 'landed_price':None},
                      {'fob_price':0.09, 'landed_price':None}, 
                      {'fob_price':None, 'landed_price':None},
                      {'fob_price':0.05, 'landed_price':None},
                      {'fob_price':None, 'landed_price':None}, 
                      {'fob_price':0.14, 'landed_price':None}]
        median = self.drug_searcher.get_median_prices(price_list)
        self.assertAlmostEquals(0.09, median[0])

    def test_none_values_ignored_when_calculating_median_landed_price_of_list(self):
        price_list = [{'landed_price':None, 'fob_price':None},
                      {'landed_price':0.09, 'fob_price':None}, 
                      {'landed_price':None, 'fob_price':None},
                      {'landed_price':0.05, 'fob_price':None},
                      {'landed_price':None, 'fob_price':None}, 
                      {'landed_price':0.14, 'fob_price':None}]
        median = self.drug_searcher.get_median_prices(price_list)
        self.assertAlmostEquals(0.09, median[1])

    def get_amitrilon_25(self):
        products = self.drug_searcher.get_products_based_on_formulation_with_id(1)
        
        amitrilon25 = products[0]
        
        return amitrilon25

    def test_amitrilon_25_returned_as_product_based_on_amitryptyline(self):
        amitrilon25 = self.get_amitrilon_25()
        self.assertEquals("AMITRILON-25", amitrilon25['product'])

    def test_afrifarmacia_and_aspen_returned_as_suppliers_of_amitryptyline(self):
        amitrilon25 = self.get_amitrilon_25()
        
        afrifarmacia = {'name':u"Afrifármacia, Lda", 'url':"/suppliers/1/test"}
        aspen_pharmacare = {'name':"Aspen Pharmacare Ltd, S.A", 'url':"/suppliers/2/test"}
        
        expected_suppliers = [afrifarmacia, aspen_pharmacare]
        
        self.assertEquals(expected_suppliers, amitrilon25['suppliers'])
        