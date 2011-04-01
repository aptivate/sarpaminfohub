from django.core.exceptions import ObjectDoesNotExist

from sarpaminfohub.infohub.backend import Backend
from sarpaminfohub.infohub.models import Formulation, Supplier, Price, \
    ProductRegistration

class DjangoBackend(Backend):
    def get_msh_price_from_formulation(self, formulation):
        try:
            msh_price = formulation.mshprice.price
        except ObjectDoesNotExist:
            msh_price = None
            
        return msh_price
    
    def get_formulations_that_match(self, search_term):
        # pylint:disable-msg=E1101
        prices = Price.objects.filter(formulation__name__icontains=search_term)

        results = []

        for price in prices:
            results.append(price.get_record())

        return results

    def get_prices_for_formulation_with_id(self, formulation_id):
        # pylint:disable-msg=E1101
        prices = Price.objects.filter(formulation=formulation_id)

        results = []

        for price in prices:
            results.append(price.get_record())

        return results

    def get_formulation_name_with_id(self, formulation_id):
        # pylint:disable-msg=E1101
        formulation = Formulation.objects.get(pk=formulation_id)

        return formulation.name

    def get_formulation_msh_with_id(self, formulation_id):
        # pylint:disable-msg=E1101
        formulation = Formulation.objects.get(pk=formulation_id)
        return self.get_msh_price_from_formulation(formulation)

    def get_product_registrations_based_on_formulation_with_id(self,
                                                               formulation_id):
        # pylint:disable-msg=E1101
        registrations = ProductRegistration.objects.filter(product__formulation=formulation_id)
        
        results = []
        
        for registration in registrations:
            record = {}
            record['product'] = registration.product.get_record()
            if registration.supplier != None:
                supplier_record = registration.supplier.get_record()
            else:
                supplier_record = None
                
            record['supplier'] = supplier_record
            
            if registration.manufacturer != None:
                manufacturer_record = registration.manufacturer.get_record()
            else:
                manufacturer_record = None

            record['manufacturer'] = manufacturer_record 
            record['country'] = registration.country.get_record()
            results.append(record)
            
        return results

    def get_registrations_from_supplier_with_id(self, supplier_id):
        # pylint:disable-msg=E1101
        return [registration for registration
            in ProductRegistration.objects.filter(supplier=supplier_id)]

    def get_products_from_supplier_with_id(self, supplier_id):
        registrations = self.get_registrations_from_supplier_with_id(supplier_id)

        results = []

        for reg in registrations:
            results.append(reg.product.get_formulation_record())

        return results

    def get_name_of_supplier_with_id(self, supplier_id):
        # pylint:disable-msg=E1101
        supplier = Supplier.objects.get(pk=supplier_id)
        return supplier.name
