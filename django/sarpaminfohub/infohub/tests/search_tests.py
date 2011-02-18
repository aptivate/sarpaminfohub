from django.test import TestCase

class SearchTest(TestCase):
    def test_search_page_is_based_on_search_template(self):
        response = self.client.get('/');
        self.assertTemplateUsed(response, 'search.html')
