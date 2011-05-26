from django.contrib.auth.models import User
from tagging.models import Tag
from sarpaminfohub.contactlist.tests.contactlist_test_case import ContactListTestCase

class SearchTest(ContactListTestCase):
    login_user = None
    contact1 = None
    contact2 = None
    contact3 = None
    
    def login(self, client):
        if self.login_user is None:
            self.login_user = User.objects.create_user(
                            'admin',
                            'sarpaminfohub-team@aptivate.org',
                            password='aptivate'
                        )
            self.assertTrue(client.login(
                            username='admin',
                            password='aptivate'))
    def setUp(self):
        self.delete_contacts()
        self.create_contacts()
        self.rebuild_search_index()

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
        # pylint:disable-msg=E1101
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
        response = client.post(self.get_contacts_url(self.contact3),{})
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
        
        response = client.post('/contacts/', {"tags":tag_ids})
        self.assertContains(response, 'My Name')
        self.assertNotContains(response, "Aptivate")
        
    def get_contacts_url(self, contact):
        return "/contacts/%d/" % contact.id
        