import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class ProductTable(SarpamTable):
    product = tables.Column()
    suppliers = tables.Column()

    def __init__(self, rows):
        tables.MemoryTable.__init__(self, rows, order_by='product')
    
    def get_rows_template(self):
        return "supplier_rows.html"
