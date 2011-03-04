from sarpaminfohub.infohub.backend import Backend

class TestBackend(Backend):
    def get_amitriptyline(self):
        return self.get_formulation_for_country("amitriptyline",
                                                country="Namibia", 
                                                fob_price=58.64, 
                                                currency='NAD',
                                                period=2009, 
                                                issue_unit=500, 
                                                landed_price=67.44, 
                                                formulation_id=8)
    
    def get_ciprofloxacin(self):
        return self.get_formulation_for_country("ciprofloxacin 500mg tablet", 
                                                country="South Africa", 
                                                fob_price=3.74, 
                                                currency='ZAR', 
                                                period=2009, 
                                                issue_unit=10, 
                                                landed_price=3.74, 
                                                formulation_id=20)
        ciprofloxacin = {"formulation":"ciprofloxacin 500mg tablet",
             "fob_price":"3.74",
             "landed_price":"3.74",
             "country":"South Africa",
             "fob_currency":"ZAR",
             "period":"2009",
             "issue_unit":"10",
             "landed_currency":"ZAR"}
        return ciprofloxacin
    
    def get_amitriptyline_with_issue_unit_none(self):
        amitriptyline = self.get_amitriptyline()
        amitriptyline['issue_unit'] = None
        return amitriptyline

    def get_formulation_for_country(self, name, country, fob_price=None, 
                                    currency=None, period=None, 
                                    issue_unit=None, landed_price=None,
                                    formulation_id=None):
        
        url = "/formulation/%d/" % formulation_id
        
        return {'formulation':name, 'country':country, 'fob_price': fob_price,
                'fob_currency':currency, 'period':period, 
                'issue_unit':issue_unit, 'landed_price':landed_price, 
                'landed_currency':currency,
                'url':url}
    
    def get_amoxycillin125_for_country(self, country, 
                                       fob_price=None, 
                                       currency=None, period=None, 
                                       issue_unit=None, landed_price=None):
        return self.get_formulation_for_country("amoxycillin 125mg/5ml suspension",
                                                country, fob_price, 
                                                currency, period, 
                                                issue_unit, landed_price,
                                                formulation_id=9)
    
    def get_amoxycillin500_for_country(self, country):
        return self.get_formulation_for_country("amoxycillin 500mg tablet/capsule",
                                                country,
                                                formulation_id=10)
        
    def get_tamoxifen_for_country(self, country):
        return self.get_formulation_for_country("tamoxifen 20mg tablet",
                                                country, formulation_id=49)
    
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
        test_result = {'fob_price': 58.64,
                       'landed_price': 67.44,
                       'country': "Namibia",
                       'fob_currency': "NAD",
                       'period': 2009,
                       'issue_unit': 500,
                       'landed_currency': "NAD"}
        
        return [test_result]
    
    def get_formulation_name_with_id(self,formulation_id):
        return "ciprofloxacin 500mg tablet"
