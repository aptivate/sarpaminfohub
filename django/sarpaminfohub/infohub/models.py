from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

class Formulation(models.Model):
    name = models.CharField(max_length=200)

    def get_url(self):
        return reverse('formulation-by-id', args=[str(self.id), ""])

    def get_msh_price(self):
        try:
            msh_price = self.mshprice.price
        except ObjectDoesNotExist:
            msh_price = None
            
        return msh_price

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)
    
    def get_record(self):
        record = {}
        record['name'] = self.name
        return record
    
class Price(models.Model):
    formulation = models.ForeignKey(Formulation)
    country = models.ForeignKey(Country)
    fob_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    landed_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    fob_currency = models.CharField(max_length=3, null=True)
    period = models.IntegerField()
    issue_unit = models.FloatField(null=True)
    landed_currency = models.CharField(max_length=3, null=True)

    def get_record(self):
        record = {}
        record['formulation'] = self.formulation.name
        record['country'] = self.country.name
        record['fob_price'] = self.fob_price
        record['landed_price'] = self.landed_price
        record['msh_price'] = self.formulation.get_msh_price()
        record['fob_currency'] = self.fob_currency
        record['period'] = self.period
        record['issue_unit'] = self.issue_unit
        record['landed_currency'] = self.landed_currency
        record['url'] = self.formulation.get_url()
        return record

class ExchangeRate(models.Model):
    symbol = models.CharField(max_length=3)
    year = models.IntegerField()
    rate = models.FloatField()

class MSHPrice(models.Model):
    formulation = models.OneToOneField(Formulation)
    period = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=6, null=True)

class Supplier(models.Model):
    name = models.CharField(max_length=200)

    def get_url(self):
        return reverse('suppliers', args=[str(self.id), ""])

    def get_record(self):
        record = {}
        record['name'] = self.name
        record['url'] = self.get_url()       
        return record

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)

    def get_record(self):
        record = {}
        record['name'] = self.name
        return record

class Product(models.Model):
    formulation = models.ForeignKey(Formulation)
    name = models.CharField(max_length=200)

    def get_formulation_record(self):
        record = {}
        record['product'] = self.name
        record['formulation_name'] = self.formulation.name
        record['formulation_url'] = self.formulation.get_url()
        return record

class ProductRegistration(models.Model):
    product = models.ForeignKey(Product)
    supplier = models.ForeignKey(Supplier, null=True)
    country = models.ForeignKey(Country)
    manufacturer = models.ForeignKey(Manufacturer, null=True)
