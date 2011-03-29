from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.models import Incoterm

class IncotermTest(SarpamTestCase):
    def test_name_can_be_set_and_retrieved(self):
        incoterm = Incoterm(name="FOB")
        self.assertEquals("FOB", incoterm.name)