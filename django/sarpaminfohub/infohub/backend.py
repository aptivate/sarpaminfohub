import inspect

class Backend(object):
    def abstract(self):
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')

    def search(self, search_term):
        self.abstract()
