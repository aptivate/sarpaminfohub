import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class SupplierCatalogueTable(SarpamTable):
    product = tables.Column()
    formulation_name = tables.Column(verbose_name="Formulation")

    def get_rows_template(self):
        return "supplier_catalogue_rows.html"
