from django.test.testcases import TestCase
class TemplateTest(TestCase):
    def test_iframe_contacts_template_used(self):
        response = self.load_iframe_and_return_response()
        self.assertTemplateUsed(response, "iframe/contacts.html")

    def test_iframe_src_set_correctly(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "<iframe src=\"/contacts/\"")

    def test_iframe_link_set_correctly(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "<a href=\"/contacts/\"")

    def test_iframe_page_contains_title(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "Expert Search", count=2)
        
    def load_iframe_and_return_response(self):
        response = self.client.get('/contacts/iframe/')
        return response
