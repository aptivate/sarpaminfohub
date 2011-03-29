# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
import sarpaminfohub.infohub.utils as utils

class UtilsTest(SarpamTestCase):
    def test_none_returned_for_median_of_empty_list(self):
        empty_list = []
        median = utils.get_median(empty_list)
        self.assertEquals(None, median)

    def test_middle_value_returned_for_median_of_list_with_odd_length(self):
        price_list = [0.09, 0.05, 0.14]
        median = utils.get_median(price_list)
        self.assertAlmostEquals(0.09, median)
        
    def test_average_of_middle_values_returned_for_median_of_list_with_even_length(self):
        price_list = [0.04, 0.05, 0.14, 0.07]
        median = utils.get_median(price_list)
        self.assertAlmostEquals(0.06, median)

    def test_none_values_ignored_when_calculating_median_fob_price_of_list(self):
        price_list = [{'fob_price':None, 'landed_price':None},
                      {'fob_price':0.09, 'landed_price':None}, 
                      {'fob_price':None, 'landed_price':None},
                      {'fob_price':0.05, 'landed_price':None},
                      {'fob_price':None, 'landed_price':None}, 
                      {'fob_price':0.14, 'landed_price':None}]
        median = utils.get_median_prices(price_list)
        self.assertAlmostEquals(0.09, median[0])

    def test_none_values_ignored_when_calculating_median_landed_price_of_list(self):
        price_list = [{'landed_price':None, 'fob_price':None},
                      {'landed_price':0.09, 'fob_price':None}, 
                      {'landed_price':None, 'fob_price':None},
                      {'landed_price':0.05, 'fob_price':None},
                      {'landed_price':None, 'fob_price':None}, 
                      {'landed_price':0.14, 'fob_price':None}]
        median = utils.get_median_prices(price_list)
        self.assertAlmostEquals(0.09, median[1])
