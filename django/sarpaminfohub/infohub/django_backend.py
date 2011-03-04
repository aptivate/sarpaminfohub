from sarpaminfohub.infohub.backend import Backend
from models import Price
from sarpaminfohub.infohub.models import Formulation

class DjangoBackend(Backend):
    def get_formulations_that_match(self, search_term):
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
    
    def get_prices_for_formulation_with_id(self, formulation_id):
        results = []
        
        prices = Price.objects.filter(formulation=formulation_id)
        
        for price in prices:
            record = {}
            results.append(record)
            record['country'] = price.country.name
            record['fob_price'] = price.fob_price
            record['landed_price'] = price.landed_price
            record['fob_currency'] = price.fob_currency
            record['period'] = price.period
            record['landed_currency'] = price.landed_currency
            record['issue_unit'] = price.issue_unit
        
        return results
    
    def get_formulation_name_with_id(self, formulation_id):
        formulation = Formulation.objects.get(pk=formulation_id)
        
        return formulation.name
