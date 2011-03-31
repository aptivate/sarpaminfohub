from copy import deepcopy
import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.template.loader import render_to_string
from sarpaminfohub.infohub import utils
from django.conf import settings

class FormulationGraph(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price")
    landed_price = tables.Column(verbose_name="Landed Price")
    max_price = 0.001
    NO_DATA = ""
    median_fob_price = 0.0
    median_landed_price = 0.0

    def __init__(self, rows, msh_price=None):
        # Don't like this, but rows is being modified below, causing side effects
        rows = deepcopy(rows)
        
        if msh_price is not None:
            # msh_price might be a Decimal, which max() thinks is larger than
            # any float, so in order to compare properly with floats we need
            # to convert msh_price to float as well
            self.max_price = max(self.max_price, float(msh_price)) 

        # print "input data = %s" % rows        
        (self.median_fob_price, self.median_landed_price) = \
            utils.get_median_prices(rows)
        # print "median prices = %s, %s" % (self.median_fob_price, self.median_landed_price)
        
        for row in rows:
            new_max_price = max(self.max_price, row['fob_price'], 
                row['landed_price'])
            # logging.warning("max of %s, %s and %s is %s" %
            #    (self.max_price, row['fob_price'], row['landed_price'],
            #        new_max_price))
            self.max_price = new_max_price
            
            self.round_to_set_decimal_places(row, 'fob_price')
            self.round_to_set_decimal_places(row, 'landed_price')

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
        extra_context = {
            'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
            'sarpam_number_rounding':settings.SARPAM_NUMBER_ROUNDING,
            'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE,
            'table':self,
            'msh_price':self.msh_price,
            'median_fob_price':self.median_fob_price,
            'median_landed_price':self.median_landed_price
        }
        return render_to_string('formulation/graph.html', 
            extra_context)

