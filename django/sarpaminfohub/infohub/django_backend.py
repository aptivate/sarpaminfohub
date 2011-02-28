from sarpaminfohub.infohub.backend import Backend
from models import Price

class DjangoBackend(Backend):
    def search(self, search_term):
        prices = Price.objects.filter(formulation__name__icontains=search_term)
        
        results = []
        
        for price in prices:
            record = {}
            results.append(record)
            record['formulation'] = price.formulation.name
            record['country'] = price.country.name
            record['fob_price'] = price.fob_price
            record['landed_price'] = price.landed_price
            record['fob_currency'] = price.fob_currency
            record['period'] = price.period
            record['issue_unit'] = price.issue_unit
            record['landed_currency'] = price.landed_currency
            
        return results