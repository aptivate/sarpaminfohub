from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.menu import Menu

class MenuTest(SarpamTestCase):
    def test_html_rendered_as_list(self):
        prices_tab = {'href':None, 'text' : "Prices"}
        products_tab = {'href': "/formulation_products/1", 'text': "Products"}
        entries = [prices_tab, products_tab]
        menu = Menu(entries)
        html = menu.as_html()
        
        expected_prices_li = "<li class=\"selected\">Prices</li>"
        expected_products_a = "<a href=\"/formulation_products/1\">Products</a>"
        expected_products_li = "<li>" + expected_products_a + "</li>"
        
        expected_lis = expected_prices_li + expected_products_li
        
        expected_html = "<ul class=\"menu\">" + expected_lis + "</ul>"
        
        self.assertEquals(expected_html, html)
