from django.db import models
import custom_fields
DESIGNATION = (
(1, 'Dr'),
(2, 'Honorable'),
(3, 'Mr'),
(4, 'Ms'),
(5, 'Miss'),
(6, 'Mrs'),
(7, 'Sir'),
(8, 'Madam'),
)

class Contact(models.Model):
    designation = models.CharField(max_length=1,choices=DESIGNATION)
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
    roles = models.ManyToManyField("RoleTag")
    @models.permalink
    def get_absolute_url(self):
        return ('client', (), {'id': self.id})
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class RoleTag(models.Model):
    role_name = models.CharField(max_length=64)