# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.backend import Backend

class TestBackend(Backend):
    def get_amitriptyline(self):
        return self.get_formulation_for_country("amitriptyline 25mg tablet",
                                                country="Namibia", 
                                                fob_price=58.64, 
                                                currency='NAD',
                                                period=2009, 
                                                issue_unit=500, 
                                                landed_price=67.44, 
                                                formulation_id=8,
                                                incoterm="CIF",
                                                supplier="Aspen Pharmacare Ltd, S.A",
                                                supplier_country="South Africa",
                                                manufacture_country="Netherlands",
                                                volume=10000)
    
    def get_ciprofloxacin(self):
        return self.get_formulation_for_country("ciprofloxacin 500mg tablet", 
                                                country="South Africa", 
                                                fob_price=3.74, 
                                                currency='ZAR', 
                                                period=2009, 
                                                issue_unit=10, 
                                                landed_price=3.74, 
                                                msh_price=0.033,
                                                formulation_id=20)
    
    def get_amitriptyline_with_issue_unit_none(self):
        amitriptyline = self.get_amitriptyline()
        amitriptyline['issue_unit'] = None
        return amitriptyline

    def get_formulation_for_country(self, name, country, fob_price=None, 
                                    currency=None, period=None, 
                                    issue_unit=None, landed_price=None,
                                    msh_price=None, incoterm=None,
                                    supplier=None,
                                    formulation_id=None,
                                    supplier_country=None,
                                    manufacture_country=None,
                                    volume=None):
        
        url = "/formulation/%d/" % formulation_id
        
        return {'formulation':name, 'country':country, 'fob_price': fob_price,
                'fob_currency':currency, 'period':period, 
                'issue_unit':issue_unit, 'landed_price':landed_price, 
                'msh_price':msh_price,
                'landed_currency':currency,
                'url':url,
                'incoterm':incoterm,
                'supplier':supplier,
                'supplier_country':supplier_country,
                'manufacture_country':manufacture_country,
                'volume':volume}
    
    def get_amoxycillin125_for_country(self, country, 
                                       fob_price=None, 
                                       currency=None, period=None, 
                                       issue_unit=None, landed_price=None):
        return self.get_formulation_for_country("amoxycillin 125mg/5ml suspension",
                                                country, fob_price, 
                                                currency, period, 
                                                issue_unit, landed_price,
                                                msh_price=0.005,
                                                formulation_id=9)
    
    def get_amoxycillin500_for_country(self, country):
        return self.get_formulation_for_country("amoxycillin 500mg tablet/capsule",
                                                country,
                                                msh_price=0.04,
                                                formulation_id=10)
        
    def get_tamoxifen_for_country(self, country):
        return self.get_formulation_for_country("tamoxifen 20mg tablet",
                                                country,
                                                msh_price=0.077,
                                                formulation_id=49)
    
    def get_amox(self):
        amoxycillin125_angola = self.get_amoxycillin125_for_country(country="Angola")
        amoxycillin125_botswana = self.get_amoxycillin125_for_country(
            country="Botswana",
            fob_price=0.87872,
            currency="USD",
            period=2007,
            issue_unit=100,
            landed_price=0.87872)
        amoxycillin125_drc = self.get_amoxycillin125_for_country(
            country="DRC",
            fob_price=0.29,
            currency="EUR",
            period=2009,
            issue_unit=100,
            landed_price=0.326)
        amoxycillin125_namibia = self.get_amoxycillin125_for_country(
            country="Namibia",
            fob_price=4.36,
            currency="NAD",
            period=2009,
            issue_unit=100,
            landed_price=4.93)
        
        amoxycillin500_angola = self.get_amoxycillin500_for_country("Angola")
        amoxycillin500_botswana = self.get_amoxycillin500_for_country("Botswana")
         
        tamoxifen_angola = self.get_tamoxifen_for_country("Angola")
        return [amoxycillin125_angola, amoxycillin125_botswana, 
                amoxycillin125_drc, amoxycillin125_namibia,
                amoxycillin500_angola, 
                amoxycillin500_botswana,
                tamoxifen_angola]
    
    def get_formulations_that_match(self, search_term):
        if search_term == "amitriptyline":
            amitriptyline = self.get_amitriptyline() 
            formulations = [amitriptyline] 
        elif search_term == "issue unit none":
            amitriptyline = self.get_amitriptyline_with_issue_unit_none()
            formulations = [amitriptyline]
        elif search_term == "amox":
            formulations = self.get_amox()
        else:
            ciprofloxacin = self.get_ciprofloxacin()
            formulations = [ciprofloxacin]

        return formulations

    def get_prices_for_formulation_with_id(self, formulation_id):
        amitriptyline_namibia = self.get_amitriptyline()
        amitriptyline_za = self.get_amitriptyline()
        amitriptyline_za['country'] = "South Africa"
        amitriptyline_za['fob_price'] = None
        amitriptyline_za['landed_price'] = 1234.56
        amitriptyline_za['landed_currency'] = "USD"
        amitriptyline_za['issue_unit'] = 1
        
        return [amitriptyline_namibia, amitriptyline_za]
    
    def get_formulation_name_with_id(self, formulation_id):
        return "amitriptyline 25mg tablet"

    def get_formulation_msh_with_id(self, formulation_id):
        return 0.0057

    def get_product_registrations_based_on_formulation_with_id(self,
                                                               formulation_id):
        return self.get_amitrilon25_registrations()        
    
    def get_products_from_supplier_with_id(self, supplier_id):
        amitrilon25 = {}
        amitrilon25['product'] = "AMITRILON-25"
        amitrilon25['formulation_name'] = "amitriptyline 25mg tablet"
        amitrilon25['formulation_url'] = "/formulation/1/test"

        products = [amitrilon25]
        return products

    def get_registrations_from_supplier_with_id(self, supplier_id):
        return [reg for reg in self.get_amitrilon25_registrations()
            if reg['supplier']['id'] == 1]

    def get_amitrilon25_registrations(self):
        afrifarmacia = {'id': 1,
                        'name':u"Afrifármacia, Lda",
                        'url':"/suppliers/1/test"}
        
        aspen_pharmacare = {'id': 2,
                            'name':"Aspen Pharmacare Ltd, S.A",
                            'url':"/suppliers/2/test"}

        stallion = {'name':"STALLION LABORATORIES LTD-INDIA"}

        nibia = {'name':"Nibia"}
        samgola = {'name':"Samgola"}
        
        amitriptyline = {'id': 10,
            'name': 'amitriptyline 25mg tablet'}
        
        amitrilon25 = {'id': 1,
            'name': 'AMITRILON-25',
            'formulation': amitriptyline}

        amitrolline = {'id': 3,
            'name': 'Amitrolline',
            'formulation': amitriptyline}
        
        registration1 = {'product':amitrilon25, 
                         'supplier':afrifarmacia,
                         'manufacturer':stallion,
                         'country':nibia} 

        registration2 = {'product':amitrilon25, 
                         'supplier':aspen_pharmacare,
                         'manufacturer':stallion,
                         'country':samgola} 

        registration3 = {'product':amitrolline, 
                         'supplier':afrifarmacia,
                         'manufacturer':stallion,
                         'country':samgola} 

        return [registration1, registration2, registration3]

    def get_name_of_supplier_with_id(self, supplier_id):
        return u"Afrifármacia, Lda"
