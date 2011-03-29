# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.test_backend import TestBackend
from sarpaminfohub.infohub.drug_searcher import DrugSearcher

class DrugSearcherTest(SarpamTestCase):
    def setUp(self):
        test_backend = TestBackend()
        self.drug_searcher = DrugSearcher(test_backend)
    
    def test_prices_converted_to_usd(self):
        self.set_up_exchange_rate_for_nad()
        
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
        self.set_up_exchange_rate_for_nad()
        self.set_up_exchange_rate_for_usd()
        
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
        self.set_up_exchange_rate_for_eur()
        self.set_up_exchange_rate_for_nad()
        self.set_up_exchange_rate_for_usd()
        
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

    def test_amitrilon_25_returned_as_product_based_on_amitryptyline(self):
        registrations = self.get_amitrilon_25_registrations()
        self.assertEquals("AMITRILON-25", registrations[0]['product']['name'])
        self.assertEquals("AMITRILON-25", registrations[1]['product']['name'])

    def test_afrifarmacia_and_aspen_returned_as_suppliers_of_amitryptyline(self):
        registrations = self.get_amitrilon_25_registrations()
        
        afrifarmacia = {'id': 1, 'name':u"Afrifármacia, Lda",
            'url':"/suppliers/1/test"}
        aspen_pharmacare = {'id': 2, 'name':"Aspen Pharmacare Ltd, S.A",
            'url':"/suppliers/2/test"}
        
        self.assertEquals(afrifarmacia, registrations[0]['supplier'])
        self.assertEquals(aspen_pharmacare, registrations[1]['supplier'])
        
    def test_stallion_laboratories_returned_as_manufacturer_of_amitryptyline(self):
        registrations = self.get_amitrilon_25_registrations()
        
        stallion = {'name':"STALLION LABORATORIES LTD-INDIA"}
        
        self.assertEquals(stallion, registrations[0]['manufacturer'])
        self.assertEquals(stallion, registrations[1]['manufacturer'])

    def get_amitrilon_25_registrations(self):
        registrations = self.drug_searcher.get_product_registrations_based_on_formulation_with_id(1)
        
        return registrations

    def test_amitrilon_25_returned_as_product_supplied_by_afrifarmacia(self):
        products = self.drug_searcher.get_products_from_supplier_with_id(1)

        amitrilon25 = {}
        amitrilon25['product'] = "AMITRILON-25"
        amitrilon25['formulation_name'] = "amitriptyline 25mg tablet"
        amitrilon25['formulation_url'] = "/formulation/1/test"

        expected_products = [amitrilon25]
        self.assertEquals(expected_products, products)
