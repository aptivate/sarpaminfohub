import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.conf import settings

class FormulationTable(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price (%s)"%settings.SARPAM_CURRENCY_CODE)
    landed_price = tables.Column(verbose_name="Landed Price (%s)"%settings.SARPAM_CURRENCY_CODE)

    def __init__(self, rows):
        for row in rows:
            self.round_to_set_decimal_places(row, 'fob_price')
            self.round_to_set_decimal_places(row, 'landed_price')
                        
        SarpamTable.__init__(self, rows, order_by='landed_price')

    def get_rows_template(self):
        return "formulation_rows.html"

