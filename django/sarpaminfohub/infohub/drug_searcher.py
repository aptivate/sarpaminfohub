from sarpaminfohub.infohub.currency_exchange import CurrencyExchange
import utils

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

    def get_formulations_that_match(self, search_term):
        formulations = self.backend.get_formulations_that_match(search_term)

        formulation_dict = {}
        formulation_hrefs = {}
        formulation_mshs = {}

        for formulation in formulations:
            name = formulation['formulation']

            if not name in formulation_dict:
                formulation_dict[name] = []
                formulation_hrefs[name] = formulation['url']
                formulation_mshs[name] = formulation['msh_price']

            self.convert_prices_to_usd(formulation)
            formulation_dict[name].append(formulation)

        rows = []

        for name in sorted(formulation_dict.iterkeys()):
            (median_fob_price, median_landed_price) = \
                utils.get_median_prices(formulation_dict[name])

            href = formulation_hrefs[name]
            msh_price = formulation_mshs[name]

            row = {'formulation': name,
                   'fob_price': median_fob_price,
                   'landed_price': median_landed_price,
                   'msh_price': msh_price,
                   'href': href}
            rows.append(row)

        return rows

    def get_prices_for_formulation_with_id(self, formulation_id):
        formulations = self.backend.get_prices_for_formulation_with_id(formulation_id)

        for formulation in formulations:
            self.convert_prices_to_usd(formulation)

        return formulations

    def get_formulation_name_with_id(self, formulation_id):
        return self.backend.get_formulation_name_with_id(formulation_id)

    def get_formulation_msh_with_id(self, formulation_id):
        return self.backend.get_formulation_msh_with_id(formulation_id)

    def get_product_registrations_based_on_formulation_with_id(self,
                                                               formulation_id):
        return self.backend.get_product_registrations_based_on_formulation_with_id(formulation_id)

    def get_products_from_supplier_with_id(self, supplier_id):
        return self.backend.get_products_from_supplier_with_id(supplier_id)

    def get_registrations_from_supplier_with_id(self, supplier_id):
        return self.backend.get_registrations_from_supplier_with_id(supplier_id)

    def get_name_of_supplier_with_id(self, supplier_id):
        return self.backend.get_name_of_supplier_with_id(supplier_id)
