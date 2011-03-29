from sarpaminfohub.infohub.formulation_table import FormulationTable
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase

class FormulationTableTest(TableTestCase):
    FIRST_ROW = 0
    
    COUNTRY_COLUMN = 0
    FOB_PRICE_COLUMN = 1
    LANDED_PRICE_COLUMN = 2
    
    def setUp(self):
        raw_data = [{
                 "fob_price":"3.12345678",
                 "landed_price":"4.98765432",
                 "country":"South Africa"}]

        self.formulation_table = FormulationTable(raw_data)
        rows = self.formulation_table.rows
        self.first_row = rows[self.FIRST_ROW]
    
    def test_country_stored_in_first_column(self):
        country = self.get_nth_value(self.first_row, self.COUNTRY_COLUMN)
        self.assertEquals("South Africa", country)

    def test_fob_price_stored_in_second_column(self):
        fob_price = float(self.get_nth_value(self.first_row, self.FOB_PRICE_COLUMN))
        self.assertAlmostEquals(3.123, fob_price)

    def test_landed_price_stored_in_third_column(self):
        landed_price = float(self.get_nth_value(self.first_row, self.LANDED_PRICE_COLUMN))
        self.assertAlmostEquals(4.988, landed_price)

    def test_html_includes_table(self):
        self.check_html_includes_table(self.formulation_table)

    def test_ordered_by_landed_price(self):
        self.check_ordered_by(self.formulation_table, 'landed_price')
