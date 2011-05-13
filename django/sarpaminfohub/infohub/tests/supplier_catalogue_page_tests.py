# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.page_display_test_case import PageDisplayTestCase
class SupplierCataloguePageTest(PageDisplayTestCase):
    def test_page_uses_correct_template(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.assertTemplateUsed(response, 'supplier_catalogue.html')

    def test_products_supplied_by_afrifarmacia_includes_amitrilion25(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.assertContains(response, "AMITRILON-25")
        
    def test_products_supplied_by_afrifarmacia_includes_amitriptyline25mgtablet(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.check_link_visible_on_page(response, href="/formulation/10/test", 
            text="amitriptyline 25mg tablet", count=2)
            
    def test_products_tab_is_selected(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.check_tab_is_selected(response, "Product Catalogue")

    def test_search_field_visible_on_page(self):
        self.check_search_field_visible_on_page('/suppliers/1/test')
        
    def test_supplier_name_appears_above_table(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.check_sub_sub_title_is(response, u"Afrifármacia, Lda")
        
    def test_sub_title_is_supplier(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.check_sub_title_is(response, "Supplier")
        
        
    def test_registration_country_appears_in_table(self):
        response = self.load_page_with_products_supplied_by_afrifarmacia()
        self.assertContains(response, "<th>Registered In</th>")
        self.assertContains(response, "<td class=\"second\">Nibia</td>", count=1)
        self.assertContains(response, "<td class=\"second\">Samgola</td>", count=1)
        
    def load_page_with_products_supplied_by_afrifarmacia(self):
        response = self.client.get('/suppliers/1/test')
        return response
