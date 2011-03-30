from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.sarpam_table import SarpamTable
class SarpamTableTest(SarpamTestCase):
    def test_rounds_to_three_decimal_places(self):
        table = SarpamTable(None)
        test_data = [0.12346]
        first_column = 0
        table.round_to_set_decimal_places(test_data, first_column)
        
        self.assertAlmostEquals(0.123, float(test_data[first_column])) 
        
    def test_no_data_return_when_none_value_rounded(self):
        table = SarpamTable(None)
        test_data = [None]
        first_column = 0
        table.round_to_set_decimal_places(test_data, first_column)
        
        self.assertEquals("--", test_data[first_column])
 
        