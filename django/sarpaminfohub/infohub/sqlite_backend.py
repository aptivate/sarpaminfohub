from sarpaminfohub.infohub.backend import Backend
import sqlite3

class SqliteBackend(Backend):
    PMA_DATA_FILE = 'sarpam_pma.sqlite'
    
    def __init__(self):
        try:
            open(self.PMA_DATA_FILE)
        except IOError as e:
            print("({})".format(e))

        self.connection = sqlite3.connect(self.PMA_DATA_FILE)
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
    
    def do_query(self, query, params):
        self.cursor.execute(query, params)
        
    def search(self, search_term):
        query = """SELECT f10.description FROM form10_row AS f10
        INNER JOIN country ON f10.country = country.id
        WHERE f10.description LIKE ?
        ORDER BY f10.description, country.name"""
        
        params = ['%' + search_term + '%']
        self.do_query(query, params)

        results = []
        
        for row in self.cursor:
            molecule_record = {}
            results.append(molecule_record)
            molecule = row[0]
            molecule_record['molecule'] = molecule 
            
        return results
    