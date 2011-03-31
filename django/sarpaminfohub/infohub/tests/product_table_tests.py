# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase
from sarpaminfohub.infohub.product_table import ProductTable
class ProductTableTest(TableTestCase):
    FIRST_ROW = 0
    SECOND_ROW = 1
    
    PRODUCT_COLUMN = 0
    SUPPLIER_COLUMN = 1
    MANUFACTURER_COLUMN = 2
    COUNTRY_COLUMN = 3
    
    def setUp(self):
        first_record = self.create_and_return_record(product="AMITRILON-25",
                                                     supplier=u"Afrifármacia, Lda",
                                                     manufacturer="STALLION LABORATORIES LTD-INDIA",
                                                     country="Nibia")
        second_record = self.create_and_return_record(product="AMITRILON-25",
                                                      supplier="Aspen Pharmacare Ltd, S.A",
                                                      manufacturer="STALLION LABORATORIES LTD-INDIA",
                                                      country="Samgola")
        supplier_records = [first_record, second_record]                                              

        self.product_table = ProductTable(supplier_records)
        rows = self.product_table.rows
        self.first_row = rows[self.FIRST_ROW]
        self.second_row = rows[self.SECOND_ROW]
    
    def create_and_return_record(self, product, supplier, manufacturer, country):
        record = {"product":product,
                  "supplier":supplier,
                  "manufacturer":manufacturer,
                  "country":country}
        return record
        
    def test_product_name_stored_in_first_column_of_first_row(self):
        product_name = self.get_nth_value(self.first_row, self.PRODUCT_COLUMN)
        self.assertEquals("AMITRILON-25", product_name)

    def test_product_name_stored_in_first_column_of_second(self):
        product_name = self.get_nth_value(self.second_row, self.PRODUCT_COLUMN)
        self.assertEquals("AMITRILON-25", product_name)

    def test_supplier_stored_in_second_column_of_first_row(self):
        supplier = self.get_nth_value(self.first_row, self.SUPPLIER_COLUMN)        
        self.assertEquals(u"Afrifármacia, Lda", supplier)

    def test_supplier_stored_in_second_column_of_second_row(self):        
        supplier = self.get_nth_value(self.second_row, self.SUPPLIER_COLUMN)
        self.assertEquals(u"Aspen Pharmacare Ltd, S.A", supplier)
        
    def test_manufacturer_stored_in_third_column_of_first_row(self):
        manufacturers = self.get_nth_value(self.first_row,
                                           self.MANUFACTURER_COLUMN)
        self.assertEquals("STALLION LABORATORIES LTD-INDIA", manufacturers)

    def test_manufacturer_stored_in_third_column_of_second_row(self):
        manufacturers = self.get_nth_value(self.second_row,
                                           self.MANUFACTURER_COLUMN)
        self.assertEquals("STALLION LABORATORIES LTD-INDIA", manufacturers)

    def test_country_stored_in_fourth_column_of_first_row(self):
        countries = self.get_nth_value(self.first_row, self.COUNTRY_COLUMN)
        self.assertEquals("Nibia", countries)

    def test_country_stored_in_fourth_column_of_second_row(self):
        countries = self.get_nth_value(self.second_row, self.COUNTRY_COLUMN)
        self.assertEquals("Samgola", countries)

    def test_html_includes_table(self):
        self.check_html_includes_table(self.product_table)

    def test_sorted_by_product_name(self):
        self.check_ordered_by(self.product_table, 'product')

    def test_table_has_correct_number_of_columns(self):
        num_columns = len(self.product_table.columns)
        self.assertEquals(4, num_columns)

    def test_verbose_name_for_country_is_registered_in(self):
        country_column = self.get_nth_value(self.product_table.columns,
                                            self.COUNTRY_COLUMN)
        self.assertEquals("Registered In", unicode(country_column))
