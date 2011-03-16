from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from itertools import islice

class TableTestCase(SarpamTestCase):
    def get_nth_value(self, iterable, n, default=None):
        return next(islice(iterable, n, None), default)
    
    def contains(self, string_to_search, sub_string):
        return string_to_search.find(sub_string) > -1

    def check_html_includes_table(self, table):
        html = table.as_html()
        self.assertTrue(self.contains(html, "<table class=\"data\">"))
        self.assertTrue(self.contains(html, "</table>"))

    def check_ordered_by(self, table, order):
        order_by = table.order_by
        expected_order = (order,)
        self.assertEquals(expected_order, order_by)