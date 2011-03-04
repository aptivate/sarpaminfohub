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

    def get_expected_price_table_cell(self, price):
        return '<td class="number">%s</td>' % \
            round(float(price),3)

    def test_fob_price_appears_right_aligned_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "FOB Price");
        
        fob_price_in_nad = 58.64
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        expected_output = self.get_expected_price_table_cell(fob_price_in_usd)
        
        self.assertContains(response, expected_output)

    def test_landed_price_appears_right_aligned_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "Landed Price");
        
        landed_price_in_nad = 67.44
        exchange_rate = 0.12314
        issue_unit = 500
        
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
        expected_output = self.get_expected_price_table_cell(landed_price_in_usd)
        
        self.assertContains(response, expected_output)

    def test_formulation_name_appears_above_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "ciprofloxacin 500mg tablet");
