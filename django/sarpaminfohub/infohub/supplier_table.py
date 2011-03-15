import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class SupplierTable(SarpamTable):
    product = tables.Column()
    suppliers = tables.Column()

    def get_rows_template(self):
        return "supplier_rows.html"
