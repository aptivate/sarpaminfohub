import inspect

class Backend(object):
    def abstract(self):
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')

    # pylint: disable-msg=W0613
    def get_formulations_that_match(self, search_term):
        self.abstract()

    def get_prices_for_formulation_with_id(self, formulation_id):
        self.abstract()
        
    def get_formulation_name_with_id(self, formulation_id):
        self.abstract()

    def get_product_registrations_based_on_formulation_with_id(self,
                                                               formulation_id):
        self.abstract()

    def get_products_from_supplier_with_id(self, supplier_id):
        self.abstract()

    def get_name_of_supplier_with_id(self, supplier_id):
        self.abstract()
