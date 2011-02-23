import django_tables as tables
from django.template.loader import render_to_string

class ResultsTable(tables.MemoryTable):
    molecule = tables.Column()
    product = tables.Column()
    formulation = tables.Column()
    price = tables.Column()
    country = tables.Column()

    def __init__(self, rows, search_string):
        tables.MemoryTable.__init__(self, rows)
        self.search_string = search_string

    def as_html(self):
        return render_to_string('results.html',\
                                {'table':self, \
                                 'search_string':self.search_string})
    