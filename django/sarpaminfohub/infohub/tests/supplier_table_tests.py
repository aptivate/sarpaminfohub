# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.table_test_case import TableTestCase
from sarpaminfohub.infohub.supplier_table import SupplierTable
class SupplierTableTest(TableTestCase):
    FIRST_ROW = 0
    
    PRODUCT_COLUMN = 0
    SUPPLIER_COLUMN = 1
    
    def setUp(self):
        suppliers = u"Afrifármacia, Lda, Aspen Pharmacare Ltd, S.A"
        
        supplier_records = [{
                 "product":"AMITRILON-25",
                 "suppliers":suppliers}]

        self.supplier_table = SupplierTable(supplier_records)
        rows = self.supplier_table.rows
        self.first_row = rows[self.FIRST_ROW]
    
    def test_product_name_stored_in_first_column(self):
        product_name = self.get_nth_value(self.first_row, self.PRODUCT_COLUMN)
        
        self.assertEquals("AMITRILON-25", product_name)

    def test_suppliers_stored_in_second_column(self):
        supplier = self.get_nth_value(self.first_row, self.SUPPLIER_COLUMN)
        
        self.assertEquals(u"Afrifármacia, Lda, Aspen Pharmacare Ltd, S.A",
                          supplier)

    def test_html_includes_table(self):
        self.check_html_includes_table(self.supplier_table)

    def test_sorted_by_product_name(self):
        self.check_ordered_by(self.supplier_table, 'product')
