from django.test import TestCase

from sarpaminfohub.infohub.forms import SearchForm

class SearchTest(TestCase):
    def test_search_page_is_based_on_search_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'search.html')

    def test_search_form_can_be_created(self):
        search_form = SearchForm()
        self.assertTrue(isinstance(search_form, SearchForm))

    def test_search_form_has_search_field(self):
        search_form = SearchForm()
        self.assertTrue(search_form.fields.has_key('search'))
