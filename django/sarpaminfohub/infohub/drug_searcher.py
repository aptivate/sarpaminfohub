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
    
    def convert_prices_to_usd(self, formulation):
        fob_local_price = self.float_or_none(formulation['fob_price'])
        fob_currency = formulation['fob_currency']
        period = formulation['period']
        issue_unit = self.int_or_none(formulation['issue_unit'])
    
        formulation['fob_price'] = self.unit_price_in_usd(fob_local_price,
                                                  fob_currency,
                                                  period, 
                                                  issue_unit)

        landed_local_price = self.float_or_none(formulation['landed_price'])
        landed_currency = formulation['landed_currency']

        formulation['landed_price'] = self.unit_price_in_usd(landed_local_price, 
                                                     landed_currency, 
                                                     period, 
                                                     issue_unit)

    def get_median(self, values):
        num_set = len(values)
    
        if num_set > 0:
            sorted_values = sorted(values)
            
            (mid_point, remainder) = divmod(num_set,2)
            
            if remainder == 1:
                median = sorted_values[mid_point]
            else:
                median = (sorted_values[mid_point] + sorted_values[mid_point - 1]) / 2
        else:
            median = None
            
        return median

    def get_median_prices(self, formulations):
        fob_prices = []
        landed_prices = []
        
        for formulation in formulations:
            fob_price = formulation['fob_price']
            landed_price = formulation['landed_price']
            
            if fob_price != None:
                fob_prices.append(fob_price)

            if landed_price != None:
                landed_prices.append(landed_price)

        median_fob_price = self.get_median(fob_prices)
        median_landed_price = self.get_median(landed_prices)

        return (median_fob_price, median_landed_price)
    
    def get_formulations_that_match(self, search_term):
        formulations = self.backend.get_formulations_that_match(search_term)
        
        formulation_dict = {}
        
        for formulation in formulations:
            name = formulation['formulation']
            
            if not name in formulation_dict:
                formulation_dict[name] = [] 

            self.convert_prices_to_usd(formulation)
            formulation_dict[name].append(formulation)

        rows = []

        for name in sorted(formulation_dict.iterkeys()):
            (median_fob_price, median_landed_price) = \
                self.get_median_prices(formulation_dict[name])
            
            row = {'formulation':name, 'fob_price':median_fob_price,
                   'landed_price':median_landed_price}
            rows.append(row)

        return rows

    def get_prices_for_formulation_with_id(self, formulation_id):
        formulations = self.backend.get_prices_for_formulation_with_id(formulation_id)
        
        for formulation in formulations:
            self.convert_prices_to_usd(formulation)
        
        return formulations
            
    def get_formulation_name_with_id(self, formulation_id):
        return self.backend.get_formulation_name_with_id(formulation_id)
        