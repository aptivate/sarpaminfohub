from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class DisplayFormulationTest(SarpamTestCase):
    def test_display_formulation_uses_correct_template(self):
        response = self.client.get('/formulation/1/test')
        self.assertTemplateUsed(response, 'formulation.html')

    def test_country_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "Country")
        self.assertContains(response, "South Africa")

    def test_fob_price_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "FOB Price");
        self.assertContains(response, "0.009")

    def test_landed_price_appears_in_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "Landed Price");
        self.assertContains(response, "0.01")

    def test_formulation_name_appears_above_formulation_table(self):
        response = self.client.get('/formulation/1/test')
        self.assertContains(response, "ciprofloxacin 500mg tablet");
