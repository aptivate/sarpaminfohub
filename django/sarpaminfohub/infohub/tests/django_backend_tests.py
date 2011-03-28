from sarpaminfohub.infohub.django_backend import DjangoBackend
from decimal import Decimal
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.models import Country, Supplier, Manufacturer,\
    ProductRegistration
from django.core.urlresolvers import reverse

class DjangoBackendTest(SarpamTestCase):
    
    def setUp(self):
        self.backend = DjangoBackend()
        
        self.expected_ciprofloxacin_results = \
            {"formulation":"ciprofloxacin 500mg tablet",
             "country": "Democratic Republic of Congo",
             "msh_price": Decimal("0.033000"),
             "fob_price": Decimal("0.000003"),
             "landed_price": Decimal("0.000004"),
             "fob_currency": 'EUR',
             "period": 2009,
             "issue_unit":100,
             "landed_currency": 'EUR'}

        self.ciprofloxacin = self.set_up_and_return_drc_ciprofloxacin(fob_price=Decimal("0.000003"),
                                     landed_price=Decimal("0.000004"))
        self.expected_ciprofloxacin_results['url'] = reverse('formulation-by-id',
            args=[self.ciprofloxacin.id, ""])
        
        self.biofloxx = self.set_up_and_return_biofloxx(self.ciprofloxacin)
    
    def test_search_for_ciprofloxacin_returns_ciprofloxacin_500mg(self):
        self.set_up_msh_for_ciprofloxacin()
        results = self.backend.get_formulations_that_match('ciprofloxacin')
        self.assertEquals(self.expected_ciprofloxacin_results, results[0])

    def test_search_is_case_insensitive(self):
        results = self.backend.get_formulations_that_match('CIPROFLOXACIN')
        first_row = results[0]
        self.assertEquals(self.expected_ciprofloxacin_results['formulation'],
                          first_row['formulation'])

    def get_first_row_of_prices_with_formulation_id_1(self):
        rows = self.backend.get_prices_for_formulation_with_id(1)
        return rows[0]

    def check_column_matches_expected_field_with_name(self, name):
        first_row = self.get_first_row_of_prices_with_formulation_id_1()
        self.assertEquals(self.expected_ciprofloxacin_results[name],
                          first_row[name])

    def test_ciprofloxacin_country_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('country')

    def test_ciprofloxacin_fob_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('fob_price')

    def test_ciprofloxacin_landed_price_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('landed_price')

    def test_ciprofloxacin_fob_currency_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('fob_currency')
        
    def test_ciprofloxacin_period_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('period')
        
    def test_ciprofloxacin_issue_unit_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('issue_unit')
        
    def test_ciprofloxacin_issue_landed_currency_can_be_retrieved_by_id(self):
        self.check_column_matches_expected_field_with_name('landed_currency')

    def test_formulation_name_can_be_retrieved_by_id(self):
        name = self.backend.get_formulation_name_with_id(1)
        self.assertEquals("ciprofloxacin 500mg tablet", name)

    def test_formulation_msh_can_be_retrieved_by_id(self):
        self.set_up_msh_for_ciprofloxacin()
        msh_price = self.backend.get_formulation_msh_with_id(1)
        self.assertEquals(self.expected_ciprofloxacin_results['msh_price'], 
                          msh_price)

    def test_ciprofloxacin_product_can_be_retrieved_by_id(self):
        self.set_up_minimal_biofloxx_registrations()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        self.assertEquals("BIOFLOXX 500 MG", registrations[0]['product'])

    def test_ciprofloxacin_suppliers_can_be_retrieved_by_id(self):
        self.set_up_biofloxx_registrations_with_suppliers_and_manufacturers()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        biotech_labs = {'name' : "Biotech Laboratories",
                                'url' : "/suppliers/1/"}
        
        camox = {'name' : "Camox Pharmaceuticals (Pty) Ltd",
                 'url' : "/suppliers/2/"}
        
        self.assertEquals(biotech_labs, registrations[0]['supplier'])
        self.assertEquals(camox, registrations[1]['supplier'])

    def test_null_suppliers_can_be_retrieved_by_id(self):
        self.set_up_minimal_biofloxx_registrations()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        self.assertEquals(None, registrations[0]['supplier'])
        self.assertEquals(None, registrations[1]['supplier'])

    def test_null_manufacturers_can_be_retrieved_by_id(self):
        self.set_up_minimal_biofloxx_registrations()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        self.assertEquals(None, registrations[0]['manufacturer'])
        self.assertEquals(None, registrations[1]['manufacturer'])


    def test_ciprofloxacin_manufacturers_can_be_retrieved_by_id(self):
        self.set_up_biofloxx_registrations_with_suppliers_and_manufacturers()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        unique_pharma = {'name' : "Unique Pharmaceutical Labs, India"}
        
        self.assertEquals(unique_pharma, registrations[0]['manufacturer'])
        self.assertEquals(unique_pharma, registrations[1]['manufacturer'])

    def test_ciprofloxacin_countries_can_be_retrieved_by_id(self):
        self.set_up_minimal_biofloxx_registrations()
        registrations = self.get_product_registrations_based_on_ciprofloxacin()
        
        nibia = {'name':"Nibia"}
        samgala = {'name':"Samgala"}

        self.assertEquals(nibia, registrations[0]['country'])
        self.assertEquals(samgala, registrations[1]['country'])

    def test_supplier_name_can_be_retrieved_by_id(self):
        biotech = self.set_up_and_return_biotech_labs()
        supplier_name = self.backend.get_name_of_supplier_with_id(biotech.id)
        self.assertEquals("Biotech Laboratories", supplier_name)

    def test_msh_price_none_for_formulation_with_no_msh(self):
        first_row = self.get_first_row_of_prices_with_formulation_id_1()
        self.assertEquals(None, first_row['msh_price'])

    def test_msh_price_none_for_matching_formulation_with_no_msh(self):
        results = self.backend.get_formulations_that_match('ciprofloxacin')
        first_row = results[0]
        self.assertEquals(None, first_row['msh_price'])
    
    def test_biofloxx_returned_as_a_product_supplied_by_biotech_labs(self):
        self.set_up_biofloxx_registrations_with_suppliers_and_manufacturers()
        products = self.backend.get_products_from_supplier_with_id(self.biotech_labs.id)
        
        biofloxx = {'product' : "BIOFLOXX 500 MG",
                    'formulation_name' : "ciprofloxacin 500mg tablet",
                    'formulation_url' : "/formulation/1/"}

        expected_products = [biofloxx]
        
        self.assertEquals(expected_products, products)
    
    def get_product_registrations_based_on_ciprofloxacin(self):
        registrations = self.backend.get_product_registrations_based_on_formulation_with_id(1)
        return registrations

    def set_up_biofloxx_registrations_with_suppliers_and_manufacturers(self):
        nibia = self.set_up_and_return_nibia()
        samgala = self.set_up_and_return_samgala()
        unique_pharma = self.set_up_and_return_unique_pharma()
        self.biotech_labs = self.set_up_and_return_biotech_labs()
        self.camox = self.set_up_and_return_camox()
        
        self.set_up_biofloxx_registration(manufacturer=unique_pharma, 
                                          supplier=self.biotech_labs, country=nibia)
        self.set_up_biofloxx_registration(manufacturer=unique_pharma, 
                                          supplier=self.camox, country=samgala)
        
    def set_up_minimal_biofloxx_registrations(self):
        nibia = self.set_up_and_return_nibia()
        samgala = self.set_up_and_return_samgala()

        self.set_up_biofloxx_registration(manufacturer=None, 
                                          supplier=None, country=nibia)
        self.set_up_biofloxx_registration(manufacturer=None, 
                                          supplier=None, country=samgala)

        
    def set_up_biofloxx_registration(self, manufacturer, supplier, country):
        registration = ProductRegistration(product=self.biofloxx,
                                           manufacturer=manufacturer,
                                           supplier=supplier,
                                           country=country)
        registration.save()
        
        
    def set_up_and_return_biotech_labs(self):
        biotech_laboratories = Supplier(name="Biotech Laboratories")
        biotech_laboratories.save()
        
        return biotech_laboratories
        
    def set_up_and_return_camox(self):
        camox_pharmaceuticals = Supplier(name="Camox Pharmaceuticals (Pty) Ltd")
        camox_pharmaceuticals.save()
        
        return camox_pharmaceuticals

    def set_up_and_return_unique_pharma(self):
        unique_pharma = Manufacturer(name="Unique Pharmaceutical Labs, India")
        unique_pharma.save()
        
        return unique_pharma

    def set_up_and_return_nibia(self):
        nibia = Country(code='NB', name='Nibia')
        nibia.save(self)
        
        return nibia
        
    def set_up_and_return_samgala(self):
        samgala = Country(code='SM', name='Samgala')
        samgala.save(self)
        
        return samgala
