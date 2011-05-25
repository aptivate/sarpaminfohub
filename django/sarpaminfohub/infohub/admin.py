from django.contrib import admin
from sarpaminfohub.infohub.models import Formulation, Incoterm, Manufacturer,\
    Supplier, Price, Country, ExchangeRate, MSHPrice, Product,\
    ProductRegistration

admin.site.register(Formulation)
admin.site.register(Country)
admin.site.register(Incoterm)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Price)
admin.site.register(ExchangeRate)
admin.site.register(MSHPrice)
admin.site.register(Product)
admin.site.register(ProductRegistration)

