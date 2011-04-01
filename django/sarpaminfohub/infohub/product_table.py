import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class ProductTable(SarpamTable):
    product = tables.Column()
    supplier = tables.Column()
    manufacturer = tables.Column()
    country = tables.Column(verbose_name="Registered In")

    def __init__(self, rows):
        SarpamTable.__init__(self, rows, order_by='product')
    
    def get_rows_template(self):
        return "product_rows.html"
