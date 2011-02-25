from django.test.testcases import TestCase
from sarpaminfohub.infohub.models import Formulation, Price, Country

class SarpamTestCase(TestCase):
    def setup_drc_ciprofloxacin(self, fob_price="0.03", landed_price="0.04"):
        ciprofloxacin = Formulation(name="ciprofloxacin 500mg tablet") 
        ciprofloxacin.save()
        
        drc = Country(code='CD', name='Democratic Republic of Congo')
        drc.save()
        
        price = Price(formulation=ciprofloxacin, country=drc, 
                      fob_price=fob_price, landed_price=landed_price)
        price.save()
