from sarpaminfohub.infohub.backend import Backend

class TestBackend(Backend):
    def get_amitriptyline(self):
        return {"formulation":"amitriptyline 25mg tablet",
                     "fob_price":"58.64",
                     "fob_currency":"NAD",
                     "landed_price":"67.44",
                     "landed_currency":"NAD",
                     "country":"Namibia",
                     "period":"2009",
                     "issue_unit":"500"}
    
    def search(self, search_term):
        if search_term == "amitriptyline":
            test_result = self.get_amitriptyline() 
        elif search_term == "issue unit none":
            test_result = self.get_amitriptyline()
            test_result['issue_unit'] = None
        else:
            test_result = {"formulation":"ciprofloxacin 500mg tablet",
                 "fob_price":"3.74",
                 "landed_price":"3.74",
                 "country":"South Africa",
                 "fob_currency":"ZAR",
                 "period":"2009",
                 "issue_unit":"10",
                 "landed_currency":"ZAR"}

        return [test_result]

    def get_prices_for_formulation_with_id(self, formulation_id):
        test_result = {"fob_price": 0.009,
                       "landed_price": 0.010,
                       "country": "South Africa"}
        
        return [test_result]
    
    def get_formulation_name_with_id(self,formulation_id):
        return "ciprofloxacin 500mg tablet"
