from django.db import models
from tagging.fields import TagField
from tagging.utils import parse_tag_input
from sarpaminfohub.contactlist.search_indexes import ContactIndex
from haystack import site
from sarpaminfohub.contactlist import custom_fields

DESIGNATION = (
('1', 'Dr'),
('2', 'Honorable'),
('3', 'Mr'),
('4', 'Ms'),
('5', 'Miss'),
('6', 'Mrs'),
('7', 'Sir'),
('8', 'Madam'),
)

class Contact(models.Model):
    """Searchable contact for the sarpaminfohub project"""
    designation = models.CharField(max_length=1,choices=DESIGNATION)
    given_name = models.CharField(max_length=128)
    family_name = models.CharField(max_length=128)
    additional_family_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=128, blank=True)
    organization = models.CharField(max_length=128, blank=True)
    address_line_1 = models.CharField(max_length=512, blank=True)
    address_line_2 = models.CharField(max_length=512, blank=True)
    address_line_3 = models.CharField(max_length=512, blank=True)
    country = custom_fields.CountryField()
    note = models.TextField(null=True, blank=True)
    tags = TagField(max_length=512)
    linked_in_url = models.URLField(unique=True,blank=True,null=True)
    linked_in_approval = models.NullBooleanField(default=None)
    access_token = models.CharField(max_length=512, blank=True)
    access_token_secret = models.CharField(max_length=512, blank=True)
    
        
    def _get_tag_list(self):
        return parse_tag_input(self.tags)
    tag_list = property(_get_tag_list)
    
    def _get_tag_hex_list(self):
        return [[tag,tag.encode('hex')] for tag in self.tag_list]
    tag_hex_list = property(_get_tag_hex_list)
    
    def get_absolute_url(self):
        return "/contacts/%d/"%self.id
    
    def __unicode__(self):
        return self.given_name + " " + self.family_name
    
    def get_full_name(self):
        full_name = u'%s %s' % (self.given_name, self.family_name)
        return full_name.strip()
    
site.register(Contact, ContactIndex)
