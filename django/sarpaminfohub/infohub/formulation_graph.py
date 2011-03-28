import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.template.loader import render_to_string
import logging

class FormulationGraph(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price")
    landed_price = tables.Column(verbose_name="Landed Price")
    max_price = 0.001
    NO_DATA = ""

    def __init__(self, rows, msh_price=None):
        if msh_price is not None:
            # msh_price might be a Decimal, which max() thinks is larger than
            # any float, so in order to compare properly with floats we need
            # to convert msh_price to float as well
            self.max_price = max(self.max_price, float(msh_price)) 
            
        for row in rows:
            new_max_price = max(self.max_price, row['fob_price'], 
                row['landed_price'])
            # logging.warning("max of %s, %s and %s is %s" %
            #    (self.max_price, row['fob_price'], row['landed_price'],
            #        new_max_price))
            self.max_price = new_max_price
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')

        # scale up the value to between 1 and 10, then round up the first
        # digit to 1, 2 or 5 to make nicer graph scales
        rounded_up = self.max_price
        scale_factor = 1

        while rounded_up < 1:
            rounded_up = rounded_up * 10
            scale_factor = scale_factor * 10
        
        while rounded_up > 10:
            rounded_up = rounded_up / 10.0
            scale_factor = scale_factor / 10.0

        if rounded_up > 5:
            rounded_up = 10.0
        elif rounded_up > 2:
            rounded_up = 5.0
        elif rounded_up > 1:
            rounded_up = 2.0
        # else it's 1, which is fine
        
        # scale back down
        self.max_price = rounded_up / scale_factor
        
        # generate the intervals on the graph scale
        self.scale = []
        for k in range(1, 11):
            self.scale.append(k * (self.max_price / 10))

        self.msh_price = msh_price

        SarpamTable.__init__(self, rows)

    def as_html(self):
        return render_to_string('formulation/graph.html',
                                {'table': self, 'msh_price': self.msh_price})

