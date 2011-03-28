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
        if msh_price is not None:
            self.max_price = msh_price 
            
        for row in rows:
            self.max_price = max(self.max_price, row['fob_price'], 
                row['landed_price'])
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')

        self.max_price = round(float(self.max_price), 3)
        
        self.scale = []
        for k in range(1, 11):
            self.scale.append(k * (self.max_price / 10))

        self.msh_price = msh_price

        SarpamTable.__init__(self, rows)

    def as_html(self):
        return render_to_string('formulation/graph.html',
                                {'table': self, 'msh_price': self.msh_price})

