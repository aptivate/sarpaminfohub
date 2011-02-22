import json

class DrugSearcher(object):
    
    def __init__(self, backend):
        self.backend = backend
    
    def get_rows(self, search_term):
        matches = self.backend.search(search_term)
        rows = json.loads(matches)
        
        return rows
