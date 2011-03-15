from sarpaminfohub.infohub.formulation_graph import FormulationGraph
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase

class FormulationGraphTest(TableTestCase):
    FIRST_ROW = 0

    COUNTRY_COLUMN = 0
    FOB_PRICE_COLUMN = 1
    LANDED_PRICE_COLUMN = 2

    def setUp(self):
        raw_data = [{
                 "fob_price":"3.12345678",
                 "landed_price":"4.98765432",
                 "country":"South Africa"},{
                 "fob_price":"4.12345678",
                 "landed_price":"5.98765432",
                 "country":"Namibia"}]

        self.formulation_graph = FormulationGraph(raw_data)
        rows = self.formulation_graph.rows
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

    def test_max_price(self):
        self.assertAlmostEquals(5.988, self.formulation_graph.max_price)

    def test_no_data_is_empty(self):
        self.assertEquals("", self.formulation_graph.NO_DATA)

    def contains(self, string_to_search, sub_string):
        return string_to_search.find(sub_string) > -1

    def test_html_includes_table(self):
        html = self.formulation_graph.as_html()
        self.assertTrue(self.contains(html, "<table class=\"graph\">"))
        self.assertTrue(self.contains(html, "</table>"))
