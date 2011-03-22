import django_tables as tables
from django.template.loader import render_to_string
import inspect
class SarpamTable(tables.MemoryTable):
    def abstract(self):
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    NO_DATA = "--"
    
    def round_to_three_decimal_places(self, row, column):
        value = row[column]
                    
        if value is None:
            value = self.NO_DATA
        else:
            # value = round(float(value), 3)
            #value = round(float(value), 3)
            value = "%.3f"%value
         
        row[column] = value

    def as_html(self):
        return render_to_string('table.html', {'table':self})

    def get_rows_template(self):
        self.abstract()
