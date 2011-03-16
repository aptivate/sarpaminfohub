"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from sarpaminfohub.contactlist.models import Contact

class SimpleTest(TestCase):
    login_user = None
    def login(self, client):
        if self.login_user is None:
            self.login_user = User.objects.create_user(
                            'admin',
                            'rimawebsites-team@aptivate.org',
                            password='aptivate'
                        )
            self.assertTrue(client.login(
                            username='admin',
                            password='aptivate'))
    def setUp(self):
        self.createContacts()
    
    def createContacts(self):
        c = Contact(given_name="My", family_name="Name", phone="(12345) 678910",
                   email="a@b.c", address_line_1="123 A Road Name, Somewhere", 
                   note="Note Very Important")
        c.save()
        c = Contact(
                   given_name="Anew", family_name="Person", phone="(54321) 123456",
                   email="d@e.f", address_line_1="456 A Road, Through the Looking Glass"
                   )
        c.save()
        c = Contact(given_name="Aptivate", family_name="Employee", phone="(32543) 523566",
                   email="g@h.i", address_line_1="999 Letsbe Avenue", note="Death Note")
        c.save()
    
    def testSearchByGivenName(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"My"})
        self.assertContains(response, 'My Name')
    
    def testSearchByFamilyName(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"Person"})
        self.assertContains(response, 'Anew Person')
    
    def testSearchByPhone(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"523566"})
        self.assertContains(response, 'Aptivate Employee')
    
    def testSearchByEmail(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"g@h.i"})
        self.assertContains(response, 'Aptivate Employee')
    
    def testSearchByAddress(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"A Road Name"})
        self.assertContains(response, 'My Name')
        
        response = client.get('/search/', {'q':"A Road"})
        self.assertContains(response, 'My Name')
        self.assertContains(response, 'Anew Person')
    
    def testSearchByNote(self):
        client = self.client
        self.login(client)
        
        response = client.get('/search/', {'q':"Note Very Important"})
        self.assertContains(response, 'My Name')
        
        response = client.get('/search/', {'q':"Note"})
        self.assertContains(response, 'My Name')
        self.assertContains(response, 'Aptivate Employee')
        
        response = client.get('/search/', {'q':""})
        self.assertContains(response, 'Search for a contact by First Name, ' +
        'Last Name, Email Address, Phone Number, Address or the content ' +
        'of notes made about them.')
        
    def testNoResults(self):
        client = self.client
        self.login(client)
        response = client.get('/search/', {'q':"Invalid String"})
        self.assertContains(response, 'No Results found.')
