'''
Created on 14 Mar 2011

@author: daniell
'''
from django.contrib import admin
from sarpaminfohub.contactlist.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('family_name','given_name','email','phone','tags')
    list_display_links = ('family_name','given_name',)
    # list_filter=('tag_list',)

admin.site.register(Contact, ContactAdmin)