from django.core.exceptions import ObjectDoesNotExist

from sarpaminfohub.infohub.backend import Backend
from sarpaminfohub.infohub.models import Formulation, Product, Supplier, Price

class DjangoBackend(Backend):
    def get_msh_price_from_formulation(self, formulation):
        try:
            msh_price = formulation.mshprice.price
        except ObjectDoesNotExist:
            msh_price = None
            
        return msh_price
    
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
            record['msh_price'] = self.get_msh_price_from_formulation(price.formulation)
            record['fob_currency'] = price.fob_currency
            record['period'] = price.period
            record['issue_unit'] = price.issue_unit
            record['landed_currency'] = price.landed_currency
            record['url'] = price.formulation.get_url()

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
            record['msh_price'] = self.get_msh_price_from_formulation(price.formulation)
            record['fob_currency'] = price.fob_currency
            record['period'] = price.period
            record['landed_currency'] = price.landed_currency
            record['issue_unit'] = price.issue_unit

        return results

    def get_formulation_name_with_id(self, formulation_id):
        formulation = Formulation.objects.get(pk=formulation_id)

        return formulation.name

    def get_formulation_msh_with_id(self, formulation_id):
        formulation = Formulation.objects.get(pk=formulation_id)
        return self.get_msh_price_from_formulation(formulation)

    def get_products_based_on_formulation_with_id(self, formulation_id):
        products = Product.objects.filter(formulation=formulation_id)
        
        results = []
        
        for product in products:
            record = {}
            record['product'] = product.name
            
            suppliers = []
            for supplier in product.suppliers.all():
                supplier_record = {}
                supplier_record['name'] = supplier.name
                supplier_record['url'] = supplier.get_url()       
                suppliers.append(supplier_record)
                
            record['suppliers'] = suppliers
            results.append(record)
            
        return results

    def get_products_from_supplier_with_id(self, supplier_id):
        products = Product.objects.filter(suppliers=supplier_id)

        results = []

        for product in products:
            record = {}
            record['product'] = product.name
            record['formulation_name'] = product.formulation.name
            record['formulation_url'] = product.formulation.get_url()

            results.append(record)

        return results

    def get_name_of_supplier_with_id(self, supplier_id):
        supplier = Supplier.objects.get(pk=supplier_id)
        return supplier.name
