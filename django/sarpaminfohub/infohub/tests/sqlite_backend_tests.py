from django.test import TestCase
from sarpaminfohub.infohub.sqlite_backend import SqliteBackend

class SqliteBackendTest(TestCase):
    def test_search_for_ciprofloxacin_returns_drc_data(self):
        backend = SqliteBackend()
        results = backend.search('ciprofloxacin')
        
        drc_index = 3
        self.assertEquals({"molecule":"ciprofloxacin 500mg tablet"}, 
                          results[drc_index])
        