import django_tables as tables
from django.template.loader import render_to_string

class ResultsTable(tables.MemoryTable):
    NO_DATA = "--"
    
    formulation = tables.Column()
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price", default=NO_DATA)
    landed_price = tables.Column(verbose_name="Landed Price", default=NO_DATA)

    def __init__(self, rows, search_string):
        tables.MemoryTable.__init__(self, rows)
        self.search_string = search_string

    def as_html(self):
        return render_to_string('results.html',\
                                {'table':self, \
                                 'search_string':self.search_string})
    