from sarpaminfohub.infohub.forms import SearchForm
from sarpaminfohub.infohub.tests.page_display_test_case import PageDisplayTestCase

class FormulationPageTest(PageDisplayTestCase):
    def setUp(self):
        self.set_up_exchange_rate_for_nad()
        self.set_up_exchange_rate_for_usd()
                
    def test_display_formulation_uses_correct_template(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.assertTemplateUsed(response, 'formulation.html')

    def test_country_appears_in_formulation_table(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.assertContains(response, "Country")
        self.assertContains(response, "Namibia")

    def get_expected_price_table_cell(self, price):
        return 'number">%.3f</td>' % \
            round(float(price),3)

    def test_fob_price_appears_right_aligned_in_formulation_table(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.assertContains(response, "FOB Price (USD)")
        
        fob_price_in_nad = 58.64
        exchange_rate = 0.12314
        issue_unit = 500
        
        fob_price_in_usd = (fob_price_in_nad * exchange_rate) / issue_unit
        expected_output = self.get_expected_price_table_cell(fob_price_in_usd)
        
        self.assertContains(response, expected_output)

    def test_landed_price_appears_right_aligned_in_formulation_table(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.assertContains(response, "Landed Price (USD)")
        
        landed_price_in_nad = 67.44
        exchange_rate = 0.12314
        issue_unit = 500
        
        landed_price_in_usd = (landed_price_in_nad * exchange_rate) / issue_unit
        expected_output = self.get_expected_price_table_cell(landed_price_in_usd)
        self.assertContains(response, expected_output)
        
        # test a drug with only a landed price, no FOB price
        expected_output = self.get_expected_price_table_cell(1234.56)
        self.assertContains(response, expected_output)

    def test_formulation_name_appears_above_formulation_table(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_sub_sub_title_is(response, "amitriptyline 25mg tablet")

    def test_form_visible_on_page(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        search_form = response.context['search_form']
        self.assertTrue(isinstance(search_form, SearchForm))
        
    def test_search_field_visible_on_page(self):
        self.check_search_field_visible_on_page('/formulation/1/test/')
        
    def test_search_form_on_formulation_page_will_create_new_search(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.assertContains(response, "<form id=\"search\" action=\"/search/\">")
        
    def test_formulation_page_has_link_to_products(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_link_visible_on_page(response, 
                                        href="/formulation_products/1/test", 
                                        text="Related Products")

    def test_procurement_prices_tab_is_selected(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_tab_is_selected(response, "Procurement Prices")
        
    def test_popup_contains_issue_unit(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, "Issue Unit", "1")
        
    def test_popup_contains_incoterm(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, "Incoterm", "CIF")
    
    def test_popup_contains_supplier(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, "Supplier", 
                                               "Aspen Pharmacare Ltd, S.A")    
    
    def test_popup_contains_supplier_country(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, "Supplier Country", 
                                               "South Africa")    
    
    def test_popup_contains_manufacture_country(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, 
                                               "Country of Manufacture", 
                                               "Netherlands")

    def test_popup_contains_volume(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_popup_field_visible_on_page(response, 
                                               "Volume", 
                                               "10000")

    def check_popup_field_visible_on_page(self, response, expected_name,
                                          expected_value):
        expected_field = "<dt>%s</dt><dd>%s</dd>" % \
            (expected_name, expected_value)
        self.assertContains(response, expected_field)
        
    def test_formulation_sub_title_appears_on_page(self):
        response = self.load_page_for_formulation_amitriptyline_prices()
        self.check_sub_title_is(response, "Formulation")

    def load_page_for_formulation_amitriptyline_prices(self):
        response = self.client.get('/formulation/1/test/')
        return response
