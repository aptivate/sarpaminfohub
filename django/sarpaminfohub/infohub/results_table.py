import django_tables as tables
from django.template.loader import render_to_string

class ResultsTable(tables.MemoryTable):
    NO_DATA = "--"
    
    formulation = tables.Column()
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price")
    landed_price = tables.Column(verbose_name="Landed Price")
    rows_template = "drug_price_rows.html"

    def round_to_three_decimal_places(self, row, column):
            value = row[column]
                        
            if value is None:
                value = self.NO_DATA
            else:
                value = round(float(value), 3)
             
            row[column] = value

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
    
