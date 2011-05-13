from sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.models import Product

class ProductTest(SarpamTestCase):
    def test_record_includes_name(self):
        product = Product(name="AMITRILON-25")
        record = product.get_record()
        self.assertEquals(product.name, record['name'])
        
    def test_record_includes_id(self):
        product = Product(name="AMITRILON-25")
        record = product.get_record()
        self.assertEquals(product.id, record['id'])