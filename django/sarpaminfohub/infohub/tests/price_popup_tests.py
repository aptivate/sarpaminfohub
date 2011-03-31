from sarpaminfohub.infohub.price_popup import PricePopup
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class PricePopupTest(SarpamTestCase):
    def test_na_displayed_when_field_is_none(self):
        empty_fields = {'issue_unit' : None,
                  'incoterm' : "",
                  'supplier' : "",
                  'supplier_country' : "",
                  'manufacture_country' : "",
                  'volume' : ""}
        popup = PricePopup(empty_fields)
        
        html = popup.as_html()
        
        self.assertTrue(self.contains(html, "<dt>Issue Unit</dt><dd>N/A</dd>"))
