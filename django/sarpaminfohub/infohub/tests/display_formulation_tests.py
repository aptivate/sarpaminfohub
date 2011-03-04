from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class DisplayFormulationTest(SarpamTestCase):
    def setUp(self):
        self.setup_exchange_rate_for_nad()
        
    def test_display_formulation_uses_correct_template(self):
        response = self.client.get('/formulation/1/test')
        self.assertTemplateUsed(response, 'formulation.html')

    def test_country_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "Country")
        self.assertContains(response, "Namibia")

    def test_fob_price_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "FOB Price");
        
        fob_price_in_nad = 58.64
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        
        self.assertContains(response, round(float(fob_price_in_usd),3))

    def test_landed_price_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "Landed Price");
        
        landed_price_in_nad = 67.44
        exchange_rate = 0.12314
        issue_unit = 500
        
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
        
        self.assertContains(response, round(float(landed_price_in_usd),3))

    def test_formulation_name_appears_above_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "ciprofloxacin 500mg tablet");
