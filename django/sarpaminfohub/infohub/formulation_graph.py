import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.template.loader import render_to_string

class FormulationGraph(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price")
    landed_price = tables.Column(verbose_name="Landed Price")
    max_price = 0
    NO_DATA = ""

    def __init__(self, rows, msh_price=None):
        for row in rows:
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')

            if isinstance(row['fob_price'], float) and row['fob_price'] > self.max_price:
                self.max_price = row['fob_price']

            if isinstance(row['landed_price'], float) and row['landed_price'] > self.max_price:
                self.max_price = row['landed_price']

        self.scale = []
        for k in range(1, 11):
            self.scale.append(k * (self.max_price / 10))

        self.msh_price = msh_price

        tables.MemoryTable.__init__(self, rows)

    def as_html(self):
        return render_to_string('formulation/graph.html',
                                {'table': self, 'msh_price': self.msh_price})

