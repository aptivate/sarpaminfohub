# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class SupplierTest(SarpamTestCase):
    def load_page_with_suppliers_of_amitriptyline(self):
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
