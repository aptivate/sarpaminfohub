import django_tables as tables
from django.template.loader import render_to_string

class ResultsTable(tables.MemoryTable):
    molecule = tables.Column()
    product = tables.Column()
    formulation = tables.Column()
    price = tables.Column()
    country = tables.Column()

    def as_html(self):
        return render_to_string('table.html', {'table':self})
    