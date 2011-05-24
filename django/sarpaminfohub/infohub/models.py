from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

class Formulation(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=50)
    strength = models.CharField(max_length=50)

    def get_url(self):
        return reverse('formulation-by-id', args=[str(self.id), ""])

    def get_msh_price(self):
        try:
            msh_price = self.mshprice.price
        except ObjectDoesNotExist:
            msh_price = None
            
        return msh_price

    def __unicode__(self):
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)
    
    def get_record(self):
        record = {}
        record['name'] = self.name
        return record

    def __unicode__(self):
        return self.name
    
class Incoterm(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=200)

    def get_record(self):
        record = {}
        record['name'] = self.name
        return record

    def __unicode__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)

    def get_url(self):
        return reverse('suppliers', args=[str(self.id), ""])

    def get_record(self):
        record = {}
        record['name'] = self.name
        record['url'] = self.get_url()       
        return record

    def __unicode__(self):
        return self.name

class Price(models.Model):
    formulation = models.ForeignKey(Formulation)
    country = models.ForeignKey(Country, null=True)
    fob_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    landed_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    fob_currency = models.CharField(max_length=3, null=True)
    period = models.IntegerField(null=True)
    issue_unit = models.FloatField(null=True)
    landed_currency = models.CharField(max_length=3, null=True)
    volume = models.IntegerField(null=True)
    incoterm = models.ForeignKey(Incoterm,null=True)
    manufacture_country = models.ForeignKey(Country,
                                             related_name='manufacture_country',
                                             null=True)
    supplier_country = models.ForeignKey(Country,
                                         related_name='supplier_country',
                                         null=True)
    supplier = models.ForeignKey(Supplier, null=True)

    def get_record(self):
        record = {}
        record['formulation'] = self.formulation.name
        
        if self.country is not None:
            country = self.country.name
        else:
            country = None
        record['country'] = country
        
        record['fob_price'] = self.fob_price
        record['landed_price'] = self.landed_price
        record['msh_price'] = self.formulation.get_msh_price()
        record['fob_currency'] = self.fob_currency
        record['period'] = self.period
        record['issue_unit'] = self.issue_unit
        record['landed_currency'] = self.landed_currency
        record['url'] = self.formulation.get_url()
        
        if self.incoterm is not None:
            incoterm = self.incoterm.name
        else:
            incoterm = None    
        record['incoterm'] = incoterm
        
        if self.supplier is not None:
            supplier = self.supplier.name
        else:
            supplier = None
        record['supplier'] = supplier
        
        if self.supplier_country is not None:
            supplier_country = self.supplier_country.name
        else:
            supplier_country = None
        record['supplier_country'] = supplier_country
        
        if self.manufacture_country is not None:
            manufacture_country = self.manufacture_country.name
        else:
            manufacture_country = None
        record['manufacture_country'] = manufacture_country

        record['volume'] = self.volume
        
        return record

    def __unicode__(self):
        return "%s %s" % (self.formulation, self.country)


class ExchangeRate(models.Model):
    symbol = models.CharField(max_length=3)
    year = models.IntegerField()
    rate = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (self.symbol, self.year)

class MSHPrice(models.Model):
    formulation = models.OneToOneField(Formulation)
    period = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=6, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.formulation, self.period)

class Product(models.Model):
    name = models.CharField(max_length=200)
    formulation = models.ForeignKey(Formulation)
    packaging = models.CharField(max_length=100)
    unit_of_issue = models.CharField(max_length=100)
    who_prequalified = models.BooleanField()

    def get_record(self):
        record = {}
        record['id'] = self.id
        record['name'] = self.name
        return record

    def get_formulation_record(self):
        record = {}
        record['product'] = self.name
        record['formulation_name'] = self.formulation.name
        record['formulation_url'] = self.formulation.get_url()
        return record

    def __unicode__(self):
        return self.name

class ProductRegistration(models.Model):
    product = models.ForeignKey(Product, related_name="registrations")
    supplier = models.ForeignKey(Supplier, null=True)
    country = models.ForeignKey(Country)
    manufacturer = models.ForeignKey(Manufacturer, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.product, self.country)
