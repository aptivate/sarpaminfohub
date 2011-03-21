from django.db import models
from tagging.fields import TagField
import custom_fields
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
    tags = TagField()
    
    def get_absolute_url(self):
        return "/contacts/%d/"%self.id
    
    def __unicode__(self):
        return self.given_name + " " + self.family_name