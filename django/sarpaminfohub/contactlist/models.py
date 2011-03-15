from django.db import models
import custom_fields
TITLES = (
(1, 'Dr'),
(1, 'Honorable'),
(1, 'Mr'),
(1, 'Ms'),
(1, 'Miss'),
(1, 'Mrs'),
(1, 'Sir'),
(1, 'Madam'),
)

class Contact(models.Model):
    title = models.CharField(length=1,choices=TITLES)
    given_name = models.CharField(max_length=128)
    family_name = models.CharField(max_length=128)
    additional_family_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=256)
    address_line_1 = models.CharField(max_length=512)
    address_line_2 = models.CharField(max_length=512)
    address_line_3 = models.CharField(max_length=512)
    country = custom_fields.CountryField()
    note = models.TextField(null=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('client', (), {'id': self.id})
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


