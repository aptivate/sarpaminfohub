import django_tables as tables
from django.template.loader import render_to_string
from sarpaminfohub.infohub.sarpam_table import SarpamTable

class ResultsTable(SarpamTable):
    formulation = tables.Column()
    fob_price = tables.Column(verbose_name="Median FOB Price")
    landed_price = tables.Column(verbose_name="Median Landed Price")
    rows_template = "drug_price_rows.html"

    def __init__(self, rows, search_string):
        for row in rows:
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')
                        
        tables.MemoryTable.__init__(self, rows)
        self.search_string = search_string

    def as_html(self):
        return render_to_string('results.html',\
                                {'table':self, \
                                 'search_string':self.search_string})
    
