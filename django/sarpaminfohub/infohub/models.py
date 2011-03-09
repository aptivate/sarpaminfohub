from django.db import models
from django.core.urlresolvers import reverse

class Formulation(models.Model):
    name = models.CharField(max_length=200)

    def get_url(self):
        return reverse('formulation', args=[str(self.id), ""])

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)
    
class Price(models.Model):
    formulation = models.ForeignKey(Formulation)
    country = models.ForeignKey(Country)
    fob_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    landed_price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    fob_currency = models.CharField(max_length=3, null=True)
    period = models.IntegerField()
    issue_unit = models.FloatField(null=True)
    landed_currency = models.CharField(max_length=3, null=True)

class ExchangeRate(models.Model):
    symbol = models.CharField(max_length=3)
    year = models.IntegerField()
    rate = models.FloatField()

class MSHPrice(models.Model):
    formulation = models.OneToOneField(Formulation)
    period = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
