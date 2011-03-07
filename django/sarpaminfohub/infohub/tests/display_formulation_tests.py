from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.forms import SearchForm

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
        response = self.client.get('/formulation/1/test', )
        self.assertContains(response, "amitriptyline");

    def test_formulation_page_has_link_to_results(self):
        response = self.client.get('/formulation/1/test/',
                                   HTTP_REFERER='/?search=amitrip')
        self.assertContains(response, 
                            "<a href=\"/?search=amitrip\">Search Results</a>")

    def test_formulation_page_does_not_link_to_referrer_from_different_http_host(self):
        response = self.client.get('/formulation/1/test/',
                                   HTTP_REFERER='http://www.google.com/')
        self.assertNotContains(response, 
                               "<a href=\"http://www.google.com/\">Search Results</a>")
        
    def test_formulation_page_does_not_link_to_referrer_from_different_https_host(self):
        response = self.client.get('/formulation/1/test/',
                                   HTTP_REFERER='https://www.google.com/')
        self.assertNotContains(response, 
                               "<a href=\"https://www.google.com/\">Search Results</a>")
        
    def test_no_search_results_when_no_referrer(self):
        response = self.client.get('/formulation/1/test/')
        self.assertNotContains(response, "Search Results")
        
    def test_form_visible_on_page(self):
        response = self.client.get('/formulation/1/test/')
        search_form = response.context['search_form']
        self.assertTrue(isinstance(search_form, SearchForm))
        
    def test_search_field_visible_on_page(self):
        response = self.client.get('/formulation/1/test/')
        self.assertContains(response,
                            "<input type=\"text\" name=\"search\" id=\"id_search\" />")
        
    def test_search_form_on_formulation_page_will_create_new_search(self):
        response = self.client.get('/formulation/1/test/')
        self.assertContains(response, "<form id=\"search\" action=\"/\">")
        
        