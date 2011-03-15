'''
Created on 14 Mar 2011

@author: daniell
'''
from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site
from sarpaminfohub.contactlist.models import Contact

class ContactIndex(RealTimeSearchIndex):
    text=CharField(document=True, use_template=True)
    given_name=CharField(model_attr="given_name")
    family_name=CharField(model_attr="family_name")
    # additional_family_name = CharField(model_attr="additional_family_name")
    address_1=CharField(model_attr="address_line_1")
    address_2=CharField(model_attr="address_line_2")
    address_3=CharField(model_attr="address_line_3")
    note=CharField(model_attr="note", null=True)
    
    # given_name = models.CharField(max_length=128)
    # family_name = models.CharField(max_length=128)
    # additional_family_name = models.CharField(max_length=128, blank=True)
    # phone = models.CharField(max_length=20, blank=True)
    # email = models.EmailField(max_length=256, blank=True)
    # address_line_1 = models.CharField(max_length=512, blank=True)
    # address_line_2 = models.CharField(max_length=512, blank=True)
    # address_line_3 = models.CharField(max_length=512, blank=True)
    # country = custom_fields.CountryField()
    # note = models.TextField(null=True, blank=True)
    # tags = TagField()
site.register(Contact, ContactIndex)