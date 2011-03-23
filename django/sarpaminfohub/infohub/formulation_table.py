import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class FormulationTable(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price (USD)")
    landed_price = tables.Column(verbose_name="Landed Price (USD)")
    rows_template = "formulation_rows.html"

    def __init__(self, rows):
        for row in rows:
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')
                        
        SarpamTable.__init__(self, rows, order_by='landed_price')

    def get_rows_template(self):
        return "formulation_rows.html"

