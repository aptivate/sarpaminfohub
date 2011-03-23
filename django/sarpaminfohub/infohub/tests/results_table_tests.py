from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase

class ResultsTableTest(TableTestCase):
    FOB_COLUMN = 1
    LANDED_COLUMN = 2
    MSH_COLUMN = 3
    
    FIRST_ROW = 0
    
    def get_cell_from_first_row_of_test_data(self, column_index):
        raw_data = \
                [{"formulation":"ciprofloxacin 500mg tablet",
                 "fob_price":"3.12345678",
                 "landed_price":"4.98765432",
                 "msh_price":"2.12345678",
                 "country":"South Africa"}]
        
        results_table = ResultsTable(raw_data, "")
        actual_rows = results_table.rows
        first_row = actual_rows[self.FIRST_ROW]

        return float(self.get_nth_value(first_row, column_index))
    
    
    def test_fob_price_displayed_with_three_decimal_places(self):
        fob_price = self.get_cell_from_first_row_of_test_data(self.FOB_COLUMN)

        self.assertAlmostEquals(3.123, float(fob_price))

    def test_landed_price_displayed_with_three_decimal_places(self):
        landed_price = self.get_cell_from_first_row_of_test_data(self.LANDED_COLUMN)

        self.assertAlmostEquals(4.988, float(landed_price))
        
    def test_msh_price_displayed_with_three_decimal_places(self):
        msh_price = self.get_cell_from_first_row_of_test_data(self.MSH_COLUMN)

        self.assertAlmostEquals(2.123, float(msh_price))
        
