from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from itertools import islice

class TableTestCase(SarpamTestCase):
    def get_nth_value(self, iterable, nn, default=None):
        return next(islice(iterable, nn, None), default)
    
    def check_html_includes_table(self, table):
        html = table.as_html()
        self.assertTrue(self.contains(html, "<table class=\"data\">"))
        self.assertTrue(self.contains(html, "</table>"))

    def check_ordered_by(self, table, order):
        order_by = table.order_by
        expected_order = (order,)
        self.assertEquals(expected_order, order_by)