from sarpaminfohub.contactlist.tests.contactlist_test_case import ContactListTestCase
class ContactListPageTestCase(ContactListTestCase):
    FLASH_MESSAGE = "<div id=\"flashmessagebox\">"
    
    def check_flash_message_appears_on_page(self, url):
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        
        self.assertContains(response, self.FLASH_MESSAGE)

    def check_flash_message_does_not_appear_on_page(self, url):
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        
        self.assertNotContains(response, self.FLASH_MESSAGE)
