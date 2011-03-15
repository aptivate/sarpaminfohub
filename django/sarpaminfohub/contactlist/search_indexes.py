'''
Created on 14 Mar 2011

@author: daniell
'''
from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site
from sarpaminfohub.contactlist.models import Contact

class ContactIndex(RealTimeSearchIndex):
    text=CharField(document=True, use_template=True)
    first_name=CharField(model_attr="first_name")
    last_name=CharField(model_attr="last_name")
    phone=CharField(model_attr="phone") 
    email=CharField(model_attr="email")
    address=CharField(model_attr="address")
    note=CharField(model_attr="note", null=True)
    
site.register(Contact, ContactIndex)