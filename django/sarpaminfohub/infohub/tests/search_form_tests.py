from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase
from sarpaminfohub.infohub.forms import SearchForm

class SearchFormTest(SarpamTestCase):
    def test_search_form_can_be_created(self):
        search_form = SearchForm()
        self.assertTrue(isinstance(search_form, SearchForm))

    def test_search_form_has_search_field(self):
        search_form = SearchForm()
        self.assertTrue(search_form.fields.has_key('search'))

    def test_search_field_has_no_label(self):
        search_form = SearchForm()
        search_field = search_form.fields['search']
        self.assertEquals("", search_field.label)

