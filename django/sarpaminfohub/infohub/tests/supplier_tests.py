# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.page_display_test_case import PageDisplayTestCase

class SupplierTest(PageDisplayTestCase):
    def load_page_with_suppliers_of_amitriptyline(self, referer=None):
        return self.client.get('/formulation_suppliers/1/test')
    
    def test_suppliers_list_uses_correct_template(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.assertTemplateUsed(response, 'formulation_suppliers.html')

    def test_suppliers_template_based_on_page_template(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.assertTemplateUsed(response, 'page.html')

    def test_suppliers_list_for_amitriptyline_includes_amitrilon_25(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.assertContains(response, "AMITRILON-25")

    def test_suppliers_list_for_amitriptyline_includes_afrifarmacia(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.assertContains(response, u"Afrifármacia, Lda")
        
    def test_suppliers_list_for_amitriptyline_includes_aspen_pharmacare(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.assertContains(response, "Aspen Pharmacare Ltd, S.A")

    def test_search_field_visible_on_page(self):
        self.check_search_field_visible_on_page('/formulation_suppliers/1/test')

    def test_page_has_link_to_prices(self):
        response = self.load_page_with_suppliers_of_amitriptyline(referer='/formulation/1/test')
        self.check_link_visible_on_page(response,
                                        href="/formulation/1/test",
                                        text="amitriptyline 25mg tablet")

    def test_products_tab_is_selected(self):
        response = self.load_page_with_suppliers_of_amitriptyline()
        self.check_tab_is_selected(response, "Products")
