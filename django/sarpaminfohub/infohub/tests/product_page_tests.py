# -*- coding: iso-8859-15 -*-
from sarpaminfohub.infohub.tests.page_display_test_case import PageDisplayTestCase
from sarpaminfohub.infohub.models import Product, Formulation,\
    ProductRegistration, Manufacturer, Country, Supplier
import sarpaminfohub.infohub.views
import django.core.urlresolvers  

class ProductPageTest(PageDisplayTestCase):
    def test_product_landing_page_contains_zovirax(self):
        self.create_zovirax()
        
        zovirax = Product.objects.get(name="ZOVIRAX 200MG DISPERSABLE TABLET")
        response = self.get(sarpaminfohub.infohub.views.product_page,
            product_name=zovirax.name)
        self.assertEqual(response.context['product'], zovirax)
        self.assertTrue(len(zovirax.registrations.all()) > 0)
        
    def test_product_landing_page_for_product_with_supplier(self):
        self.create_lovire()
        
        lovire = Product.objects.get(name="Lovire 200 Tablets")
        response = self.get(sarpaminfohub.infohub.views.product_page,
            product_name=lovire.name)
        self.assertEqual(response.context['product'], lovire)
        self.assertTrue(len(lovire.registrations.all()) > 0)
        self.assertNotEqual(None, lovire.registrations.all()[0])

    def get(self, view_function, **view_args):
        return self.client.get(django.core.urlresolvers.reverse(view_function,
            kwargs=view_args))

    def create_zovirax(self):
        aciclovir = self.create_and_return_aciclovir()
        zovirax = Product(name="ZOVIRAX 200MG DISPERSABLE TABLET",
                          formulation=aciclovir)
        zovirax.save()
        
        self.create_zovirax_registration(zovirax)
        
    def create_and_return_aciclovir(self):
        aciclovir = Formulation(name="aciclovir 200mg tablet")
        aciclovir.save()

        return aciclovir

    def create_zovirax_registration(self, zovirax):
        glaxo = Manufacturer(name="GLAXO SMITHKLINE (PTY) LTD, SA")
        glaxo.save()
        
        sangala = self.create_and_return_sangala()
        
        registration = ProductRegistration(product=zovirax, country=sangala,
                                           manufacturer=glaxo)
        registration.save()

    def create_lovire(self):
        aciclovir = self.create_and_return_aciclovir()
        
        lovire = Product(name="Lovire 200 Tablets", formulation=aciclovir)
        lovire.save()
        
        self.create_lovire_registration(lovire)
        
    def create_lovire_registration(self, lovire):
        ranbaxy = Manufacturer(name="Ranbaxy Laboratories Ltd, India")
        ranbaxy.save()
        
        sangala = self.create_and_return_sangala()
        
        supplier = Supplier(name="CIPLA MEDPRO, RSA (company name)")
        supplier.save()
        
        registration = ProductRegistration(product=lovire, country=sangala,
                                           manufacturer=ranbaxy, 
                                           supplier=supplier)
        registration.save()

    def create_and_return_sangala(self):
        sangala = Country(pk="XL", name="Sangala")
        sangala.save()

        return sangala
