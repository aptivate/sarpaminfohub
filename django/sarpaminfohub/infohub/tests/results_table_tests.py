from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.results_table import ResultsTable
from itertools import islice

class ResultsTableTest(SarpamTestCase):
    FOB_COLUMN = 2
    LANDED_COLUMN = 3
    
    FIRST_ROW = 0
    
    def get_nth_value(self, iterable, n, default=None):
        return next(islice(iterable, n, None), default)
    
    def get_cell_from_first_row_of_test_data(self, column_index):
        raw_data = \
                [{"formulation":"ciprofloxacin 500mg tablet",
                 "fob_price":"3.12345678",
                 "landed_price":"4.98765432",
                 "country":"South Africa",
                 "fob_currency":"ZAR",
                 "period":"2009",
                 "issue_unit":"10",
                 "landed_currency":"ZAR"}]
        
        results_table = ResultsTable(raw_data, "")
        actual_rows = results_table.rows
        first_row = actual_rows[self.FIRST_ROW]

        return float(self.get_nth_value(first_row, column_index))
    
    
    def test_fob_price_displayed_with_three_decimal_places(self):
        fob_price = self.get_cell_from_first_row_of_test_data(self.FOB_COLUMN)

        self.assertAlmostEquals(3.123, fob_price)

    def test_landed_price_displayed_with_three_decimal_places(self):
        landed_price = self.get_cell_from_first_row_of_test_data(self.LANDED_COLUMN)

        self.assertAlmostEquals(4.988, landed_price)
        