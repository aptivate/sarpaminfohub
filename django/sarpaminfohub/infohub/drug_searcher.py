from sarpaminfohub.infohub.currency_exchange import CurrencyExchange

class DrugSearcher(object):
    
    def __init__(self, backend):
        self.backend = backend
        self.exchanger = CurrencyExchange()
    
    def unit_price_in_usd(self, price, currency, period, issue_unit):
        if issue_unit is None:
            return None
        
        price_in_usd = self.exchanger.exchange(price, currency, period)
        
        if price_in_usd is None:
            return None
        
        return price_in_usd / issue_unit
    
    def float_or_none(self, value):
        if value is None:
            return None
        
        return float(value)
    
    def int_or_none(self, value):
        if value is None:
            return None
        
        return int(value)
    
    def get_formulations_that_match(self, search_term):
        rows = self.backend.get_formulations_that_match(search_term)
        
        for row in rows:
            fob_local_price = self.float_or_none(row['fob_price'])
            fob_currency = row['fob_currency']
            period = row['period']
            issue_unit = self.int_or_none(row['issue_unit'])
        
            row['fob_price'] = self.unit_price_in_usd(fob_local_price,
                                                      fob_currency,
                                                      period, 
                                                      issue_unit)

            landed_local_price = self.float_or_none(row['landed_price'])
            landed_currency = row['landed_currency']

            row['landed_price'] = self.unit_price_in_usd(landed_local_price, 
                                                         landed_currency, 
                                                         period, 
                                                         issue_unit)
        return rows

    def get_prices_for_formulation_with_id(self, formulation_id):
        rows = self.backend.get_prices_for_formulation_with_id(formulation_id)
        return rows
            
    def get_formulation_name_with_id(self, formulation_id):
        return self.backend.get_formulation_name_with_id(formulation_id)
        