from sarpaminfohub.contactlist.tests.contactlist_page_test_case import ContactListPageTestCase
class SearchPageTest(ContactListPageTestCase):
    def test_message_box_appears_when_specified(self):
        url = self.get_search_page_url(query_string="?deleted=true")
        self.check_flash_message_appears_on_page(url)
    
    def test_no_message_box_appears_when_not_specified(self):
        url = self.get_search_page_url()
        self.check_flash_message_does_not_appear_on_page(url)

    def get_search_page_url(self, query_string=""):
        return "/contacts/%s" % query_string
