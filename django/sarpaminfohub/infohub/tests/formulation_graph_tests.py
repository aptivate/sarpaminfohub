from sarpaminfohub.infohub.formulation_graph import FormulationGraph
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase
from decimal import Decimal
import re

class FormulationGraphTest(TableTestCase):
    FIRST_ROW = 0

    COUNTRY_COLUMN = 0
    FOB_PRICE_COLUMN = 1
    LANDED_PRICE_COLUMN = 2

    def setUp(self):
        self.raw_data = [
            dict(fob_price = 3.12345678, landed_price = 4.98765432,
                country = "South Africa"),
            dict(fob_price = 4.12345678, landed_price = 5.98765432,
                country = "Namibia")
            ]

        self.formulation_graph = FormulationGraph(self.raw_data)
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
        # round up from 5.988 to 10
        self.assertAlmostEquals(10.0, self.formulation_graph.max_price)

    def test_no_data_is_empty(self):
        self.assertEquals("", self.formulation_graph.NO_DATA)

    def contains(self, string_to_search, sub_string):
        return string_to_search.find(sub_string) > -1

    def test_html_includes_table(self):
        html = self.formulation_graph.as_html()
        self.assertTrue(self.contains(html, "<table class=\"graph\">"))
        self.assertTrue(self.contains(html, "</table>"))

    def test_graph_scale_includes_msh_price(self):
        test_graph = FormulationGraph(self.raw_data, 16.075127)
        # round up from 16.075 to 20
        self.assertAlmostEquals(20.0, test_graph.max_price)

    # Decimal seems to be larger than any float, according to max()
    def test_graph_scale_works_with_decimal_msh(self):
        test_graph = FormulationGraph(self.raw_data, Decimal('0.4577901'))
        # round up from 5.988 to 10
        self.assertAlmostEquals(10.0, test_graph.max_price)
 
    def test_graph_scale_missing_values(self):
        test_data = [
            dict(fob_price = 3.12345678, landed_price = None,
                country = "South Africa"),
            dict(fob_price = None, landed_price = 4.12345678,
                country = "Namibia")
            ]
        test_graph = FormulationGraph(test_data, None)
        # round up from 4.123 to 5
        self.assertAlmostEquals(5.0, test_graph.max_price)

    def test_graph_scale_rounding(self):
        self.assertAlmostEquals(0.001, FormulationGraph([], 0.0003).max_price)
        self.assertAlmostEquals(0.001, FormulationGraph([], 0.0005).max_price)
        self.assertAlmostEquals(0.001, FormulationGraph([], 0.0007).max_price)        
        self.assertAlmostEquals(0.001, FormulationGraph([], 0.001).max_price)
        self.assertAlmostEquals(0.1, FormulationGraph([], 0.099).max_price)
        self.assertAlmostEquals(0.1, FormulationGraph([], 0.1).max_price)
        self.assertAlmostEquals(0.2, FormulationGraph([], 0.101).max_price)
        self.assertAlmostEquals(0.2, FormulationGraph([], 0.199).max_price)
        self.assertAlmostEquals(0.2, FormulationGraph([], 0.2).max_price)
        self.assertAlmostEquals(0.5, FormulationGraph([], 0.201).max_price)
        self.assertAlmostEquals(1.0, FormulationGraph([], 0.99).max_price)
        self.assertAlmostEquals(1.0, FormulationGraph([], 1.0).max_price)
        self.assertAlmostEquals(2.0, FormulationGraph([], 1.01).max_price)
        self.assertAlmostEquals(2.0, FormulationGraph([], 1.99).max_price)
        self.assertAlmostEquals(2.0, FormulationGraph([], 2.0).max_price)
        self.assertAlmostEquals(5.0, FormulationGraph([], 4.99).max_price)
        self.assertAlmostEquals(5.0, FormulationGraph([], 5.0).max_price)
        self.assertAlmostEquals(10.0, FormulationGraph([], 5.01).max_price)
        self.assertAlmostEquals(10.0, FormulationGraph([], 9.99).max_price)
        self.assertAlmostEquals(100.0, FormulationGraph([], 50.01).max_price)
        self.assertAlmostEquals(100.0, FormulationGraph([], 99.99).max_price)
        self.assertAlmostEquals(100.0, FormulationGraph([], 100.0).max_price)

    def assertBar(self, html, name, value, scale, count):
        pattern = r'(<div class="%s[^/]*</div>)' % name
        match = re.search(pattern, html)
        self.assertTrue(match is not None)
        line = match.group(1)
        self.assertEquals(line, '<div class="%s marker" style="left:%dpx;"></div>' %
            (name,  round(value / scale * 696)))
        
        pattern = r'(<span class="%s[^/]*</span>)' % name
        match = re.search(pattern, html)
        self.assertTrue(match is not None)
        line = match.group(1)

        pattern = r'<span class="%s[^>]*>([^<]*): [^<]*</span>' % name
        match = re.search(pattern, html)
        self.assertTrue(match is not None)
        label = match.group(1)
        
        self.assertEquals(line, '<span class="%s label">%s: %.3f</span>' %
            (name, label, value))

    def test_graph_medians(self):
        data = self.raw_data[:]
        graph = FormulationGraph(data, 2.5643865)
        scale = graph.max_price
        
        # even number of data points, should average the middle two
        html = graph.as_html()
        self.assertBar(html, "msh_price", 2.564, scale, 2)
        self.assertBar(html, "median_fob_price",
            (3.12345678 + 4.12345678) / 2.0, scale, 2)
        self.assertBar(html, "median_landed_price",
            (4.98765432 + 5.98765432) / 2.0, scale, 2)
        
        # odd number of data points, should use the middle one
        data.append(dict(fob_price = 5.36789549, landed_price = 5.5367875,
                country = "Upper Eureka"))
        graph = FormulationGraph(data, 2.5643865)
        self.assertAlmostEquals(10.0, graph.max_price)
        html = graph.as_html()
        self.assertBar(html, "msh_price", 2.564, scale, 2)
        self.assertBar(html, "median_fob_price", 4.12345678, scale, 2)
        self.assertBar(html, "median_landed_price", 5.5367875, scale, 2)

        # some values missing
        data.append(dict(fob_price = 3.7854638, landed_price = None,
                country = "Lower Eureka"))
        data.append(dict(fob_price = None, landed_price = 6.3476238,
                country = "Ambata"))
        # fobs = 3.12345678, 3.7854638, 4.12345678, 5.36789549
        # landed = 4.98765432, 5.5367875, 5.98765432, 6.3476238
        graph = FormulationGraph(data, 2.5643865)
        self.assertAlmostEquals(10.0, graph.max_price)
        html = graph.as_html()
        self.assertBar(html, "msh_price", 2.564, scale, 2)
        self.assertBar(html, "median_fob_price",
            (3.7854638 + 4.12345678) / 2.0, scale, 2)
        self.assertBar(html, "median_landed_price",
            (5.5367875 + 5.98765432) / 2.0, scale, 2)
