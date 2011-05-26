from sarpaminfohub.contactlist.models import Contact
from sarpaminfohub.contactlist.tests.contactlist_page_test_case import ContactListPageTestCase

class ContactDetailPageTest(ContactListPageTestCase):
    def setUp(self):
        self.delete_contacts()
        self.create_contacts()
        self.rebuild_search_index()
    
    def test_message_box_appears_when_specified(self):
        url = self.get_contact_url(query_string="?new_contact=true")
        self.check_flash_message_appears_on_page(url)
    
    def test_no_message_box_appears_when_not_specified(self):
        url = self.get_contact_url()
        self.check_flash_message_does_not_appear_on_page(url)
    
    def get_contact_url(self, query_string=""):
        test_contact = Contact.objects.get(role="Researcher")
        
        url = "/contacts/%d/%s" % (test_contact.id, query_string)
        return url
