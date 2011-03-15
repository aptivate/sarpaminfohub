from django.db import models

class Contact(models.Model):
    given_name = models.CharField(max_length=128)
    family_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=256)
    address = models.CharField(max_length=512)
    note = models.TextField(null=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('client', (), {'id': self.id})
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


