class DrugSearcher(object):
    
    def __init__(self, backend):
        self.backend = backend
    
    def get_rows(self, search_term):
        rows = self.backend.search(search_term)
        
        return rows
