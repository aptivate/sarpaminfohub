from django.test.testcases import TestCase
from sarpaminfohub.contactlist.models import Contact
from sarpaminfohub.contactlist.profile_adder import ProfileAdder
from django.http import HttpRequest

class LinkedInTest(TestCase):
    TEST_OAUTH_TOKEN = '7ccce8fb-83e4-4ab7-b8da-7f8b5c32c4ad'
    TEST_OAUTH_VERIFIER = '75959'
    
    def test_contact_can_be_created_from_linked_in(self):
        num_contacts_before = len(Contact.objects.all())

        self.request_and_add_profile()        
        num_contacts_after = len(Contact.objects.all())
        self.assertEquals(1, num_contacts_after - num_contacts_before)

    def test_request_profile_redirects_to_auth_page(self):
        response = self.client.get('/contacts/request_linked_in_profile/testing')
        
        self.assertRedirectsNoFollow(response, 
                                     "https://api.linkedin.com/uas/oauth/authorize?oauth_token=%s" % self.TEST_OAUTH_TOKEN)

    def assertRedirectsNoFollow(self, response, expected_url):
        self.assertEqual(response._headers['location'], 
                         ('Location', expected_url))
        self.assertEqual(response.status_code, 302)

    def test_message_appears_when_token_expires(self):
        request = self.create_and_return_http_request()
        profile_adder = ProfileAdder(request, testing=True, token_timeout=0)
        profile_adder.request_profile()
        response = profile_adder.add_profile()
        self.assertContains(response, "Authorization Token Expired", 2)
    
    def request_and_add_profile(self):
        self.client.get('/contacts/request_linked_in_profile/testing')
        
        # we have to help things along a bit here as we've mocked out the
        # linked in API
        self.client.get('/contacts/add_linked_in_profile/testing?oauth_token=%s&oauth_verifier=%s' % (self.TEST_OAUTH_TOKEN, self.TEST_OAUTH_VERIFIER))

    def create_and_return_http_request(self):
        request = HttpRequest()
        request.method = 'GET'

        params = {'oauth_verifier': self.TEST_OAUTH_VERIFIER, 
                  'oauth_token': self.TEST_OAUTH_TOKEN}
        
        request.GET = params
        request.META['SERVER_NAME'] = "localhost"
        request.META['SERVER_PORT'] = 8000

        return request
