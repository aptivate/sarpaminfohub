import django_tables as tables

from django.template.loader import render_to_string
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.conf import settings

class ResultsTable(SarpamTable):
    formulation = tables.Column()
    fob_price = tables.Column(verbose_name="Median FOB Price (%s)"%settings.SARPAM_CURRENCY_CODE)
    landed_price = tables.Column(verbose_name="Median Landed Price (%s)"%settings.SARPAM_CURRENCY_CODE)
    msh_price = tables.Column(verbose_name="MSH International Median (%s)"%settings.SARPAM_CURRENCY_CODE)
    rows_template = "drug_price_rows.html"

    def __init__(self, rows, search_string):
        for row in rows:
            self.round_to_set_decimal_places(row, 'fob_price')
            self.round_to_set_decimal_places(row, 'landed_price')
            self.round_to_set_decimal_places(row, 'msh_price')

        SarpamTable.__init__(self, rows)
        self.search_string = search_string

    def as_html(self):
        return render_to_string('results.html', \
                                {'table':self, \
                                 'search_string':self.search_string})

    def get_rows_template(self):
        return "drug_price_rows.html"
