"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from sarpaminfohub.contactlist.models import Contact
from tagging.models import Tag

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
        self.contact1 = Contact(given_name="My", family_name="Name", phone="(12345) 678910",
                   email="a@b.c", address_line_1="123 A Road Name, Somewhere", 
                   role="Head of Surgery", tags="Hospital, Medicine, Surgeon", organization="London Teaching Hospital",
                   note="Note Very Important")
        self.contact1.save()
        self.contact2 = Contact(
                   given_name="Anew", family_name="Person", phone="(54321) 123456",
                   email="d@e.f", address_line_1="456 A Road, Through the Looking Glass",
                   role="Pharmacist", tags="Medicine", organization="Selby's Pharmacy"
                   )
        self.contact2.save()
        self.contact3 = Contact(given_name="Aptivate", family_name="Employee", phone="(32543) 523566",
                   email="g@h.i", address_line_1="999 Letsbe Avenue", tags="academia", note="Death Note",
                   role="Researcher", organization="Imperial College"
                   )
        self.contact3.save()
    
    def test_search_by_given_name(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"My"})
        self.assertContains(response, 'My Name')
    
    def test_search_by_family_name(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"Person"})
        self.assertContains(response, 'Anew Person')
    
    def test_search_by_note_for_name(self):
        client = self.client
        self.login(client)
        
        response = client.post('/contacts/', {'search_term':"Note Very Important"})
        self.assertContains(response, 'My Name')
    
    def test_search_has_note(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"Note"})
        self.assertContains(response, 'My Name')
        self.assertContains(response, 'Aptivate Employee')
        self.assertNotContains(response, 'Anew Person')
        
    def test_search_for_role(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"Head of Surgery"})
        self.assertContains(response, 'My Name')
        self.assertNotContains(response, 'Aptivate Employee')
        self.assertNotContains(response, 'Anew Person')
    
    def test_search_for_organization(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"London Teaching Hospital"})
        self.assertContains(response, 'My Name')
        self.assertNotContains(response, 'Aptivate Employee')
        self.assertNotContains(response, 'Anew Person')
    
    def test_search_for_name_has_role(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"My Name"})
        self.assertContains(response, "Head of Surgery")
        self.assertNotContains(response, "Pharmacist")
        self.assertNotContains(response, "Researcher")
    
    def test_search_for_name_has_organization(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"My Name"})
        self.assertContains(response, "Head of Surgery")
        self.assertNotContains(response, "Selby's Pharmacy")
        self.assertNotContains(response, "Imperial College")
    
    def test_no_results(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"Invalid String"})
        self.assertContains(response, 'No Results found.')
    
    def test_search_by_tag(self):
        client = self.client
        self.login(client)
        hospital_tag_id = Tag.objects.get(name='Hospital').id
        response = client.post('/contacts/', {'search_term':"My",
                                              "tags":[hospital_tag_id]})
        self.assertContains(response, 'My Name')
    
    def test_search_by_not_tag(self):
        client = self.client
        self.login(client)
        
        unused_tag = Tag(name="Unused")
        unused_tag.save()
        response = client.post('/contacts/', {'search_term':"My",
                                              "tags":[unused_tag.id]})
        
        self.assertContains(response, 'No Results found.')
    
    def test_search_by_tag_faux(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"My Medicine"})
        self.assertContains(response, 'My Name')
    
    def test_search_by_not_tag_faux(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/', {'search_term':"My academia"})
        self.assertContains(response, 'No Results found.')
    
    def test_contact_view_tag_presence(self):
        client = self.client
        self.login(client)
        response = client.post(self.get_contacts_url(self.contact1),{})
        self.assertContains(response,"Medicine</a></li>")
    
    def test_contact_view_tag_absence(self):
        client = self.client
        self.login(client)
        response = client.post('/contacts/3/')
        self.assertNotContains(response,"Medicine</a></li>")
    
    def test_tag_view_presence(self):
        response = self.post_tag_page_and_return_response("Medicine")
        self.assertContains(response, "My Name")
    
    def test_tag_view_absence(self):
        response = self.post_tag_page_and_return_response("Medicine")
        self.assertNotContains(response, "Aptivate")
    
    def post_tag_page_and_return_response(self, tag):
        client = self.client
        self.login(client)
        url = self.get_tags_url(tag)
        response = client.post(url)

        return response
    
    def get_tags_url(self, tag):
        return "/contacts/tags/" + tag.encode('hex') + "/"
    
    def test_multiple_tag_select(self):
        client = self.client
        self.login(client)
        
        hospital_tag_id = Tag.objects.get(name='Hospital').id
        medicine_tag_id = Tag.objects.get(name='Medicine').id
        surgeon_tag_id = Tag.objects.get(name='Surgeon').id
        
        tag_ids = [hospital_tag_id, medicine_tag_id, surgeon_tag_id]
        
        response = client.post('/contacts/',{"tags":tag_ids})
        self.assertContains(response, 'My Name')
        self.assertNotContains(response, "Aptivate")
        
    def get_contacts_url(self, contact):
        return "/contacts/%d/" % contact.id
        