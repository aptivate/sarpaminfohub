from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.models import ProductRegistration
class ProductRegistrationTest(SarpamTestCase):
    def test_supplier_may_be_null(self):
        ProductRegistration(supplier=None)

    def test_manufacturer_may_be_null(self):
        ProductRegistration(manufacturer=None)
